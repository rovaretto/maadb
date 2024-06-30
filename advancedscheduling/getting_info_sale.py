import os
import datetime
import pymongo
from bson import ObjectId
from pyomo.dataportal import DataPortal
from pyomo.opt import SolverFactory
from advancedscheduling.model import model

urlRiak = 'http://localhost:8098/riak/'

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

dbOspedale = myclient["ospedale"]

infoSale = dbOspedale["info-sale"]
#lista dei pazienti con le loro info ancora da operare: PRIMA
patient_waiting_list = dbOspedale["waiting-list"]
#lista di tutte le operazioni presenti nell'ospedale con le relative durate
duration_op = dbOspedale["duration-op"]
#planning per la settimana in costruzione: DURANTE
plan_for_week = dbOspedale["plan-for-week"]
# storico di tutti i pazienti che sono stati operati: DOPO
history = dbOspedale["operation-history"]



#planForToday: {giorno: Lunedi,
#               numeroSettimana:
#               advancedscheduling: {SalaA:"pippo","baudo",salaB:},
#                sequenziamento: {SalaA: {"Pippo":08:00,} salaB:{"Pippo":08:00,}}


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
    map_function = """
                function() {
                    emit(this._id,null)                    
                }
            """

    reduce_function = """
                function(key, values) {
                    return null;
                }
                """

    # Esegui la funzione di map-reduce
    resultDB = dbOspedale.command("mapReduce", "waiting-list", map=map_function, reduce=reduce_function, out={"inline": 1})
    res = []
    for pat in resultDB["results"]:
        res.append(str(pat['_id']))
    return res


def getDurataOperazioni(patients):
    result = {}
    for pat in patients:
        opcode = patient_waiting_list.find_one({'_id' : ObjectId(pat)}, {'opcode': 1})['opcode']
        duration = duration_op.find_one({'opcode' : opcode}, {'duration': 1})['duration']
        result[pat]= duration
    return result


def getPatientSpeciality(I):
    result = {}
    for patient in I:
        opcode = patient_waiting_list.find_one({ '_id' : ObjectId(patient)}, {'opcode': 1})['opcode']
        spec = opcode[2] + opcode[3]
        if spec == 'Ge':
            result[patient,'General'] = 1
            result[patient, 'Gyn_Obstetrics'] = 0
            result[patient, 'Otolaryngology'] = 0
            result[patient, 'Trauma'] = 0
        if spec == 'Gy':
            result[patient,'General'] = 0
            result[patient, 'Gyn_Obstetrics'] = 1
            result[patient, 'Otolaryngology'] = 0
            result[patient, 'Trauma'] = 0
        if spec == 'Ot':
            result[patient,'General'] = 0
            result[patient, 'Gyn_Obstetrics'] = 0
            result[patient, 'Otolaryngology'] = 1
            result[patient, 'Trauma'] = 0
        if spec == 'Tr':
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

print(q)

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


solver_manager = SolverFactory('cplex', executable="/opt/ibm/ILOG/CPLEX_Studio128/cplex/bin/x86-64_linux/cplex")
solver_manager.options['timelimit'] = 20

# Risolvi il problema di ottimizzazione
results = solver_manager.solve(instance)


#sposta il planning da attuale a storico
for t in instance.T:
    obj = plan_for_week.find_one({'giorno': t})
    if(obj is not None):
        plan_for_week.delete_one(obj)
        history.insert_one(obj)

patient_for_sale = {}
for t in instance.T:
    for k in instance.K:
        patient_for_sale[k] = []
        info_patient_list = []
        for i in instance.I:
            if instance.x[i,k,t].value == 1:
                info = patient_waiting_list.find_one({'_id' : ObjectId(i)})
                patient_for_sale[k].append(info)
                patient_waiting_list.delete_one({'_id': ObjectId(i)})

    obj = {'giorno' : t, 'patient_for_today' :patient_for_sale, 'numero_settimana': datetime.date.today().isocalendar()[1]}
    plan_for_week.insert_one(obj)
    print(plan_for_week.find_one({'giorno' : t}))

# {
#         'nuovo_campo': 'valore',  # Nuova voce o aggiornamento della voce esistente
#         'campo_esistente': 'nuovo_valore'  # Aggiornamento di un campo esistente
#     }
