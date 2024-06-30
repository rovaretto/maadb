from datetime import datetime, timedelta

import pymongo
import requests
from bson import ObjectId
from pyomo.core import value
from pyomo.dataportal import DataPortal

urlRiak = 'http://localhost:8098/riak/'

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

dbOspedale = myclient["ospedale"]

infoSale = dbOspedale["info-sale"]
patient_list = dbOspedale["waiting-list"]
plan_for_week = dbOspedale["plan-for-week"]
duration_op = dbOspedale["duration-op"]

def getPatient(giorno):
    map_function = f"""
        function() {{
            if(this.giorno == {giorno}){{
                for(sala in this.patient_for_today)
                    for(pat of this.patient_for_today[sala]){{
                        emit(pat._id, null);
                    }}
            }}   
        }}
        """

    reduce_function = """
        function(key, values) {
            return null;
        }
        """

    # Esegui la funzione di map-reduce
    result = dbOspedale.command("mapReduce", "plan-for-week", map=map_function, reduce=reduce_function, out={"inline": 1})
    return [str(doc['_id']) for doc in result["results"]]

def getSalaOfPatient(giorno):
    map_function = f"""
            function() {{
            if(this.giorno == {giorno}){{
                for(sala in this.patient_for_today)
                    for(pat of this.patient_for_today[sala]){{
                        emit([pat._id, sala], null);
                    }}
            }}   
        }}
        """

    reduce_function = """
            function(key, values) {
                return null;
            }
            """

    # Esegui la funzione di map-reduce
    result_from_db = dbOspedale.command("mapReduce", "plan-for-week", map=map_function, reduce=reduce_function, out={"inline": 1})["results"]
    result = {}
    for pat in result_from_db:
        result[str(pat['_id'][0])] = pat['_id'][1]
    return result

def convertToMinute(orario):
    time_obj = datetime.strptime(orario, "%H:%M")
    minutes_since_midnight = time_obj.hour * 60 + time_obj.minute
    return minutes_since_midnight

def convertToHours(orario):
    midnight = datetime.combine(datetime.today(), datetime.min.time())
    # Aggiungi i minuti alla mezzanotte
    result_time = midnight + timedelta(minutes=orario)
    return result_time.strftime("%H:%M")

def getStartSessionForPatient(giorno):
    info_sale_cursor = dbOspedale['info-sale'].find()
    orari_apertura = {item['nome']: item['orarioApertura'] for item in info_sale_cursor}
    map_function = f"""
            function() {{
                    orari_apertura = {orari_apertura}
                    if(this.giorno == {giorno}){{
                        for(sala in this.patient_for_today)
                            for(pat of this.patient_for_today[sala]){{
                                emit([pat._id,orari_apertura[sala][{giorno}]] , null);
                            }}
                    }}   
            }}
            """

    reduce_function = """
            function(key, values) {
                return null;
            }
            """

    # Esegui la funzione di map-reduce
    result_from_db = dbOspedale.command("mapReduce", "plan-for-week", map=map_function, reduce=reduce_function, out={"inline": 1})["results"]
    result = {}
    for pat in result_from_db:
        result[str(pat['_id'][0])] = convertToMinute(pat['_id'][1])
    return result

def getEndSessionForPatient(giorno):
    info_sale_cursor = dbOspedale['info-sale'].find()
    orari_chiusura = {item['nome']: item['orarioChiusura'] for item in info_sale_cursor}
    map_function = f"""
                function() {{
                        orari_chiusura = {orari_chiusura}
                        if(this.giorno == {giorno}){{
                            for(sala in this.patient_for_today)
                                for(pat of this.patient_for_today[sala]){{
                                    emit([pat._id,orari_chiusura[sala][{giorno}]] , null);
                                }}
                        }}   
                }}
                """

    reduce_function = """
            function(key, values) {
                return null;
            }
            """

    # Esegui la funzione di map-reduce
    result_from_db = dbOspedale.command("mapReduce", "plan-for-week", map=map_function, reduce=reduce_function, out={"inline": 1})["results"]
    result = {}
    for pat in result_from_db:
        result[str(pat['_id'][0])] = convertToMinute(pat['_id'][1])
    return result

def getDurataOperazioni(patients):
    result = {}
    for pat in patients:
        patient_id = ObjectId(pat)
        pipeline = [
            {
                "$project": {
                    "patient_for_today": {
                        "$objectToArray": "$patient_for_today"
                    }
                }
            },
            {
                "$unwind": "$patient_for_today"
            },
            {
                "$unwind": "$patient_for_today.v"
            },
            {
                "$match": {
                    "$expr": {
                        "$eq": ["$patient_for_today.v._id", patient_id]
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "opcode": "$patient_for_today.v.opcode"
                }
            }
        ]
        opcode = plan_for_week.aggregate(pipeline).next()['opcode']
        duration = duration_op.find_one({'opcode' : opcode}, {'duration': 1})['duration']
        result[pat]= duration
    return result

def getPatientsforSala(O):
    result ={}
    for pat in O.keys():
        res = []
        for pat2 in O.keys():
            if ( O[pat] == O[pat2]):
                res.append(pat2)
        result[pat] = res
    return result

def loader_data(giorno):
    giorno = f"\"{giorno}\""
    data = DataPortal()
    I = getPatient(giorno)
    o = getSalaOfPatient(giorno)
    s = getStartSessionForPatient(giorno)
    e = getEndSessionForPatient(giorno)
    p = getDurataOperazioni(I)
    Io = getPatientsforSala(o)

    data['I'] = I
    data['o'] = o
    data['s'] = s
    data['e'] = e
    data['p'] = p
    data['Io'] = Io
    return data

def save_result(result, data, giorno):
    for i in result.I:
        sala = result.o[i]
        print(sala)
        start_time = convertToHours(value(result.c[i]) - data['p'][i])
        # Utilizzare $set per aggiornare direttamente la chiave
        filtro = {
            "giorno": giorno,
            f"patient_for_today.{sala}._id": ObjectId(i)
        }

        aggiornamento = {
            "$set": {
                f"patient_for_today.{sala}.$[elem].operation_start_time": start_time
            }
        }

        # Define arrayFilters to match specific elements within patient_for_today
        array_filters = [{"elem._id": ObjectId(i)}]

        # Use update_one with array_filters to apply updates
        plan_for_week.update_one(filtro, aggiornamento, array_filters=array_filters)


def print_result_scheduling(giorno):
    giorno = f"\"{giorno}\""
    map_function = f"""
        function() {{        
                emit({{
                giorno : this.giorno, 
                scheduling : this.scheduling
                }}, null);  
        }}
        """

    reduce_function = """
        function(key, values) {
            return null;
        }
        """

    # Esegui la funzione di map-reduce
    result_db = dbOspedale.command("mapReduce", "plan-for-today", map=map_function, reduce=reduce_function, out={"inline": 1})
    result = {}
    print(result_db)
    for doc in result_db['results']:
        result[doc['_id']['sala']] = dict(sorted(doc['_id']['scheduling'].items(), key=lambda item: item[1]))

    for a in result:
       print(f"Giorno {a}")
       for i in result[a]:
            print(f"{i}: {result[a][i]}")
