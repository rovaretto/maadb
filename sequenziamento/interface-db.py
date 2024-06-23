from datetime import datetime

import pymongo
import requests
from pyomo.dataportal import DataPortal

urlRiak = 'http://172.30.0.2:8098/riak/'

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

dbOspedale = myclient["ospedale"]

infoSale = dbOspedale["info-sale"]
patient_list = dbOspedale["waiting-list"]


giorno = "\"Lunedi\""


def getPatient():
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



def getSalaOfPatient():
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


def convertInMinute(orario):
    time_obj = datetime.strptime(orario, "%H:%M")
    minutes_since_midnight = time_obj.hour * 60 + time_obj.minute
    return minutes_since_midnight

def getStartSessionForPatient():
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
        result[pat['_id'][0]] = convertInMinute(pat['_id'][1])
    return result

def getEndSessionForPatient():
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
        result[pat['_id'][0]] = convertInMinute(pat['_id'][1])
    return result

def getDurataOperazioni(patients):
    urlRiakPatientOperation = urlRiak + 'patients/'
    result = {}
    for pat in patients:
        opcode= pat.split("--")[1]
        duration = requests.get(urlRiakPatientOperation + opcode)
        result[pat]= duration.json()['duration']
    return result



data = DataPortal()
I = getPatient()
O = getSalaOfPatient()
s = getStartSessionForPatient()
e = getEndSessionForPatient()
p = getDurataOperazioni(I)

for a in p:
    print(p[a])
