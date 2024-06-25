import random

import pymongo
import requests

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

dbOspedale = myclient["ospedale"]

patient_list = dbOspedale["waiting-list"]
patient_list.drop()

urlRiak = 'http://localhost:8098/riak/ospedale1/' + "waiting-list"

def load():
    waiting_list_opcode = [
            'B-Ge-i-5-916.a5', 'M-Ge-i-5-987.0', 'S-Ge-i-5-98c.1', 'B-Ge-o-5-897.0', 'M-Ge-o-5-897.0', 'S-Ge-o-5-897.0',
            'B-Ge-i-5-916.a4', 'M-Ge-i-5-916.a5', 'S-Ge-i-5-983', 'B-Ge-o-5-640.2', 'M-Ge-o-5-640.2', 'S-Ge-o-5-640.2',
            'B-Ge-i-5-916.a3', 'M-Ge-i-5-916.a4', 'S-Ge-i-5-932.43', 'B-Ge-o-5-534.1', 'M-Ge-o-5-624.4', 'S-Ge-o-5-624.4',
            'B-Ge-i-5-916.a1', 'M-Ge-i-5-916.a3', 'S-Ge-i-5-932.13', 'B-Ge-o-5-534.03', 'M-Ge-o-5-534.1', 'S-Ge-o-5-535.1',
            'B-Ge-i-5-916.a0', 'M-Ge-i-5-916.a1', 'S-Ge-i-5-932.12', 'B-Ge-o-5-530.33', 'M-Ge-o-5-530.33', 'S-Ge-o-5-534.35',
            'B-Ge-i-5-900.1b', 'M-Ge-i-5-916.a0', 'S-Ge-i-5-916.a5', 'B-Ge-o-5-530.32', 'M-Ge-o-5-530.00', 'S-Ge-o-5-534.1',
            'B-Ge-i-5-897.1', 'M-Ge-i-5-911.0b', 'S-Ge-i-5-916.a4', 'B-Ge-o-5-493.2', 'M-Ge-o-5-492.00', 'S-Ge-o-5-534.03',
            'B-Ge-i-5-897.0', 'M-Ge-i-5-900.1b', 'S-Ge-i-5-916.a3', 'B-Ge-o-5-492.00', 'M-Ge-o-5-399.7', 'S-Ge-o-5-530.33',
            'B-Ge-i-5-896.1g', 'M-Ge-i-5-897.0', 'S-Ge-i-5-916.a2', 'B-Ge-o-5-399.7', 'M-Ge-o-5-399.5', 'S-Ge-o-5-530.32',
            'B-Gy-i-5-916.a0', 'M-Gy-i-5-872.1', 'S-Gy-i-8-911', 'B-Gy-o-5-870.90', 'M-Gy-o-5-870.90', 'S-Gy-o-5-870.a1',
            'B-Gy-i-5-872.1', 'M-Gy-i-5-872.0', 'S-Gy-i-5-884.2', 'B-Gy-o-5-751', 'M-Gy-o-5-751', 'S-Gy-o-5-870.a0',
            'B-Gy-i-5-872.0', 'M-Gy-i-5-870.a3', 'S-Gy-i-5-881.1', 'B-Gy-o-5-712.0', 'M-Gy-o-5-711.1', 'S-Gy-o-5-870.90',
            'B-Gy-i-5-870.a2', 'M-Gy-i-5-870.a2', 'S-Gy-i-5-877.20', 'B-Gy-o-5-711.1', 'M-Gy-o-5-691', 'S-Gy-o-5-751',
            'B-Gy-i-5-870.a1', 'M-Gy-i-5-870.a1', 'S-Gy-i-5-877.0', 'B-Gy-o-5-691', 'M-Gy-o-5-690.2', 'S-Gy-o-5-712.0',
            'B-Gy-i-5-870.a0', 'M-Gy-i-5-870.a0', 'S-Gy-i-5-872.1', 'B-Gy-o-5-690.2', 'M-Gy-o-5-690.1', 'S-Gy-o-5-711.1',
            'B-Gy-i-5-870.91', 'M-Gy-i-5-870.91', 'S-Gy-i-5-872.0', 'B-Gy-o-5-690.1', 'M-Gy-o-5-690.0', 'S-Gy-o-5-702.1',
            'B-Gy-i-5-870.90', 'M-Gy-i-5-870.90', 'S-Gy-i-5-870.a5', 'B-Gy-o-5-690.0', 'M-Gy-o-5-681.83', 'S-Gy-o-5-691',
            'B-Ot-i-5-300.7', 'M-Ot-i-5-984', 'S-Ot-i-5-766.3', 'B-Ot-o-5-300.5', 'M-Ot-o-5-300.2', 'S-Ot-o-5-285.1',
            'B-Ot-i-5-300.2', 'M-Ot-i-5-983', 'S-Ot-i-5-403.03', 'B-Ot-o-5-300.2', 'M-Ot-o-5-285.1', 'S-Ot-o-5-285.0',
            'B-Ot-i-5-289.01', 'M-Ot-i-5-892.05', 'S-Ot-i-5-403.01', 'B-Ot-o-5-285.1', 'M-Ot-o-5-285.0', 'S-Ot-o-5-216.0',
            'B-Ot-i-5-285.0', 'M-Ot-i-5-771.10', 'S-Ot-i-5-403.00', 'B-Ot-o-5-285.0', 'M-Ot-o-5-281.5', 'S-Ot-o-5-215.3',
            'B-Ot-i-5-281.5', 'M-Ot-i-5-766.3', 'S-Ot-i-5-402.0', 'B-Ot-o-5-281.5', 'M-Ot-o-5-216.1', 'S-Ot-o-5-200.5',
            'B-Ot-i-5-281.0', 'M-Ot-i-5-403.04', 'S-Ot-i-5-401.00', 'B-Ot-o-5-216.0', 'M-Ot-o-5-216.0', 'S-Ot-o-5-200.4',
            'B-Ot-i-5-280.0', 'M-Ot-i-5-403.03', 'S-Ot-i-5-319.9', 'B-Ot-o-5-215.3', 'M-Ot-o-5-200.5', 'S-Ot-o-5-194.0',
            'B-Ot-i-5-262.04', 'M-Ot-i-5-403.02', 'S-Ot-i-5-316.2', 'B-Ot-o-5-202.2', 'M-Ot-o-5-200.4', 'S-Ot-o-5-184.2',
            'B-Tr-i-5-916.a1', 'M-Tr-i-5-916.a1', 'S-Tr-i-5-986.x', 'B-Tr-o-5-859.12', 'M-Tr-o-5-812.5', 'S-Tr-o-5-983',
            'B-Tr-i-5-916.a0', 'M-Tr-i-5-916.a0', 'S-Tr-i-5-984', 'B-Tr-o-5-849.0', 'M-Tr-o-5-790.2b', 'S-Tr-o-5-849.0',
            'B-Tr-i-5-900.1f', 'M-Tr-i-5-896.1f', 'S-Tr-i-5-983', 'B-Tr-o-5-841.15', 'M-Tr-o-5-787.k6', 'S-Tr-o-5-841.14',
            'B-Tr-i-5-896.1f', 'M-Tr-i-5-896.1e', 'S-Tr-i-5-931.0', 'B-Tr-o-5-841.14', 'M-Tr-o-5-787.k0', 'S-Tr-o-5-812.5',
            'B-Tr-i-5-896.1e', 'M-Tr-i-5-869.2', 'S-Tr-i-5-916.a1', 'B-Tr-o-5-812.eh', 'M-Tr-o-5-787.gb', 'S-Tr-o-5-810.0h',
            'B-Tr-i-5-896.17', 'M-Tr-i-5-869.1', 'S-Tr-i-5-916.a0', 'B-Tr-o-5-812.5', 'M-Tr-o-5-787.3r', 'S-Tr-o-5-790.2b',
            'B-Tr-i-5-892.1e', 'M-Tr-i-5-855.19', 'S-Tr-i-5-902.4f', 'B-Tr-o-5-811.2h', 'M-Tr-o-5-787.36', 'S-Tr-o-5-790.1c',
            'B-Tr-i-5-892.0f', 'M-Tr-i-5-855.18', 'S-Tr-i-5-900.1f', 'B-Tr-o-5-811.0h', 'M-Tr-o-5-787.30', 'S-Tr-o-5-790.1b',
            'B-Tr-i-5-892.0e', 'M-Tr-i-5-855.02', 'S-Tr-i-5-896.1g', 'B-Tr-o-5-790.2b', 'M-Tr-o-5-787.1r', 'S-Tr-o-5-790.16',
            'B-Tr-i-5-869.1', 'M-Tr-i-5-83b.53', 'S-Tr-i-5-896.1f', 'B-Tr-o-5-790.1c', 'M-Tr-o-5-787.1n', 'S-Tr-o-5-787.k6']

    patient_mongo = {}
    nomi = [
        "Alessandra",
        "Luca",
        "Giulia",
        "Matteo",
        "Francesca",
        "Stefano",
        "Valentina",
        "Marco",
        "Laura",
        "Davide",
        "Federica",
        "Andrea",
        "Chiara",
        "Nicola",
        "Elisa"
    ]



    cognomi = [
        "Rossi",
        "Bianchi",
        "Colombo",
        "Ferrari",
        "Villa",
        "Fontana",
        "Rizzi",
        "Mariani",
        "Bergamaschi",
        "Bernardi",
        "Galli",
        "Greco",
        "Russo",
        "Gallo",
        "Conti"
    ]

    waiting_list = []
    i = 0
    for op in waiting_list_opcode:
        patient_mongo = {'nome' : random.choice(nomi),
                         'cognome' : random.choice(cognomi),
                         'opcode': op
                         }
        ris = patient_list.insert_one(patient_mongo)
        print(ris.inserted_id)
        waiting_list.append(f'{ris.inserted_id}--{op}')
        i += 1
    print(i)
    print(waiting_list)
    requests.post(urlRiak, json=waiting_list)
#
# mongo1: 3 * 1000 = 3000
# riak1: 1000 + 50 = 1050
# mongo2: 3 * 1050 = 3150
# riak2: 1000
# mogno3: 3 * 1100 = 3300
# riak3: 1000
#
# 1 accedi a riak e waiting-list
# 2 computi il modello
# 3 sai quali sono stati i pazienti ce verrano oiperati sta settimana
# 4 pushi la waiti-list su riak
# 5 accedi a mongo
#
# /////////
# 1 accesso a un sacco di dati di mongo

load()


#
# res = requests.get(url)
# prova = res.json()
# print(prova)
