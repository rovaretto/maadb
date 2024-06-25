from datetime import datetime, timedelta

import pymongo
import requests
from pyomo.core import value
from pyomo.dataportal import DataPortal

urlRiak = 'http://localhost:8098/riak/'

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

dbOspedale = myclient["ospedale"]

infoSale = dbOspedale["info-sale"]
patient_list = dbOspedale["waiting-list"]





def getPatient(giorno):
    map_function = f"""
        function() {{
            for(pat of this.patientPerDay[{giorno}]){{
                emit(pat, null);
            }}   
        }}
        """

    reduce_function = """
        function(key, values) {
            return null;
        }
        """

    # Esegui la funzione di map-reduce
    result = dbOspedale.command("mapReduce", "info-sale", map=map_function, reduce=reduce_function, out={"inline": 1})
    return [doc['_id'] for doc in result["results"]]



def getSalaOfPatient(giorno):
    map_function = f"""
            function() {{
                for(pat of this.patientPerDay[{giorno}]){{
                    emit([pat,this.nome] , null);
                }}   
            }}
            """

    reduce_function = """
            function(key, values) {
                return null;
            }
            """

    # Esegui la funzione di map-reduce
    result_from_db = dbOspedale.command("mapReduce", "info-sale", map=map_function, reduce=reduce_function, out={"inline": 1})["results"]
    result = {}
    for pat in result_from_db:
        result[pat['_id'][0]] = pat['_id'][1]
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
    map_function = f"""
            function() {{
                for(pat of this.patientPerDay[{giorno}]){{
                    emit([pat,this.orarioApertura[{giorno}]] , null);
                }}   
            }}
            """

    reduce_function = """
            function(key, values) {
                return null;
            }
            """

    # Esegui la funzione di map-reduce
    result_from_db = dbOspedale.command("mapReduce", "info-sale", map=map_function, reduce=reduce_function, out={"inline": 1})["results"]
    result = {}
    for pat in result_from_db:
        result[pat['_id'][0]] = convertToMinute(pat['_id'][1])
    return result

def getEndSessionForPatient(giorno):
    map_function = f"""
            function() {{
                for(pat of this.patientPerDay[{giorno}]){{
                    emit([pat,this.orarioChiusura[{giorno}]] , null);
                }}   
            }}
            """

    reduce_function = """
            function(key, values) {
                return null;
            }
            """

    # Esegui la funzione di map-reduce
    result_from_db = dbOspedale.command("mapReduce", "info-sale", map=map_function, reduce=reduce_function, out={"inline": 1})["results"]
    result = {}
    for pat in result_from_db:
        result[pat['_id'][0]] = convertToMinute(pat['_id'][1])
    return result

def getDurataOperazioni(patients):
    urlRiakPatientOperation = urlRiak + 'patients/'
    result = {}
    for pat in patients:
        opcode= pat.split("--")[1]
        duration = requests.get(urlRiakPatientOperation + opcode)
        result[pat]= duration.json()['duration']
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
        start_time = convertToHours(value(result.c[i]) - data['p'][i])
        i = i.replace(".", "_")
        # Utilizzare $set per aggiornare direttamente la chiave
        infoSale.update_one(
            {"nome": sala},
            [{"$set": {f"scheduling.{giorno}": {f"{i}": start_time}}}]
        )
    # file.write("max BIM: " + str(value(instance.h)))

def print_result_scheduling(giorno):
    giorno = f"\"{giorno}\""
    map_function = f"""
        function() {{
        
            
                emit({{
                sala : this.nome, 
                scheduling : this.scheduling[{giorno}]
                }}, null);  
        }}
        """

    reduce_function = """
        function(key, values) {
            return null;
        }
        """

    # Esegui la funzione di map-reduce
    result_db = dbOspedale.command("mapReduce", "info-sale", map=map_function, reduce=reduce_function, out={"inline": 1})
    result = {}
    for doc in result_db['results']:
        result[doc['_id']['sala']] = dict(sorted(doc['_id']['scheduling'].items(), key=lambda item: item[1]))

    for a in result:
       print(f"Sala {a}")
       for i in result[a]:
            print(f"{i}: {result[a][i]}")
