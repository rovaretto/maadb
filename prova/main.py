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

def dropAll():
    infoSale.drop()
    patient_waiting_list.drop()
    duration_op.drop()
    plan_for_week.drop()
    history.drop()

print(len([item for item in infoSale.find()]))
print(len([item for item in patient_waiting_list.find()]))
print(len([item for item in duration_op.find()]))
print(len([item for item in plan_for_week.find()]))
print(len([item for item in history.find()]))


print(([item for item in plan_for_week.find()]))