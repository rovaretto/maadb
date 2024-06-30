import os

import pymongo

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

infoSale.drop()
patient_waiting_list.drop()
duration_op.drop()
plan_for_week.drop()
history.drop()


# Esegui il primo script
os.system('python3 info_sale_loader.py')

# Esegui il secondo script
os.system('python3 loaderOperation.py')

# Esegui il terzo script
os.system('python3 patient_list_loader.py')
