import os
import re

import pymongo
import requests
from pyomo.dataportal import DataPortal
from pyomo.opt import SolverManagerFactory

from advancedscheduling.model import model

urlRiak = 'http://localhost:8098/riak/'

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

dbOspedale = myclient["ospedale"]

infoSale = dbOspedale["info-sale"]
patient_list = dbOspedale["waiting-list"]


def getSpecialita():
    map_function = """
    function() {
        for (var key in this.specialita) {
            emit(this.specialita[key], null);
        }
    }
    """

    reduce_function = """
    function(key, values) {
        return null;
    }
    """

    # Esegui la funzione di map-reduce
    result = dbOspedale.command("mapReduce", "info-sale", map=map_function, reduce=reduce_function, out={"inline": 1})
    return [doc['_id'] for doc in result["results"]]

def getDurataSale():
    map_function = """
        function() {
            for (let giorno of this.giorniApertura){
                var apertura = this.orarioApertura[giorno]
                var chiusura = this.orarioChiusura[giorno]    
                apertura = apertura.split(":")
                chiusura = chiusura.split(":")

                durata = (parseInt(chiusura[0]) - parseInt(apertura[0]))*60 + (parseInt(chiusura[1]) - parseInt(apertura[1]))
                
                emit([this.nome, giorno,durata], null);                 
        }
           
    }
    """

    reduce_function = """
        function(key, values) {
            return null;
        }
        """

    # Esegui la funzione di map-reduce
    resultDB = dbOspedale.command("mapReduce", "info-sale", map=map_function, reduce=reduce_function, out={"inline": 1})
    result = {}
    for elem in resultDB["results"]:
        tupla = elem['_id']
        result[tupla[0],tupla[1]] = tupla[2]
    return result



def getTau(J):
    map_function = """
            function() {
                for (let giorno of this.giorniApertura){
                    specToday = this.specialita[giorno]
                    emit([this.nome, giorno,specToday], null);                 
            }
        }
        """

    reduce_function = """
            function(key, values) {
                return null;
            }
            """

    # Esegui la funzione di map-reduce
    resultDB = dbOspedale.command("mapReduce", "info-sale", map=map_function, reduce=reduce_function, out={"inline": 1})
    result = {}
    for elem in resultDB["results"]:
        tupla = elem['_id']
        result[tupla[0],tupla[1], tupla[2]] = 1
        for spec in J:
            if spec != tupla[2]:
                result[tupla[0], tupla[1], spec] = 0

    return result

def getPatients():
    res = requests.get(urlRiak + 'ospedale1/waiting-list')
    return res.json()



def getDurataOperazioni(patients):
    urlRiakPatientOperation = urlRiak + 'patients/'
    result = {}
    for pat in patients:
        opcode= pat.split("--")[1]
        duration = requests.get(urlRiakPatientOperation + opcode)
        result[pat]= duration.json()['duration']
    return result


def getPatientSpeciality(I):
    result = {}
    for patient in I:

        pattern = r"(\w*)--(\w*)-(\w*)-(.*)"
        match = re.match(pattern,patient)
        if match is not None:
            if match.group(3) == 'Ge':
                result[patient,'General'] = 1
                result[patient, 'Gyn_Obstetrics'] = 0
                result[patient, 'Otolaryngology'] = 0
                result[patient, 'Trauma'] = 0
            if match.group(3) == 'Gy':
                result[patient,'General'] = 0
                result[patient, 'Gyn_Obstetrics'] = 1
                result[patient, 'Otolaryngology'] = 0
                result[patient, 'Trauma'] = 0
            if match.group(3) == 'Ot':
                result[patient,'General'] = 0
                result[patient, 'Gyn_Obstetrics'] = 0
                result[patient, 'Otolaryngology'] = 1
                result[patient, 'Trauma'] = 0
            if match.group(3) == 'Tr':
                result[patient,'General'] = 0
                result[patient, 'Gyn_Obstetrics'] = 0
                result[patient, 'Otolaryngology'] = 0
                result[patient, 'Trauma'] = 1
    return result

I = getPatients()
K = infoSale.distinct("nome")
T = infoSale.distinct("giorniApertura")
J = getSpecialita()

p = getDurataOperazioni(I)
s = getDurataSale()
q = getPatientSpeciality(I)
tau = getTau(J)


data = DataPortal()
data['I'] = I
data['K'] = K
data['T'] = T
data['J'] = J
data['p'] = p
data['s'] = s
data['q'] = q
data['tau'] = tau


instance = model.create_instance(data)
# Imposta l'indirizzo email NEOS
os.environ['NEOS_EMAIL'] = 'emanuele.rovaretto@edu.unito.it'


# Imposta il solutore su NEOS
solver_manager = SolverManagerFactory('neos')

# Risolvi il problema di ottimizzazione
results = solver_manager.solve(instance, solver="cplex", load_solutions=True)


for k in instance.K:
    result = {'Lunedi': [],
              'Martedi': [],
              'Mercoledi': [],
              'Giovedi': [],
              'Venerdi': []
              }

    for t in instance.T:
        for i in instance.I:
            if instance.x[i,k,t].value == 1:
                result[t].append(i)
    infoSale.update_one({'nome': k}, {'$set': {'patientPerDay':result}})
    print(infoSale.find_one({'nome': k}))

# {
#         'nuovo_campo': 'valore',  # Nuova voce o aggiornamento della voce esistente
#         'campo_esistente': 'nuovo_valore'  # Aggiornamento di un campo esistente
#     }
