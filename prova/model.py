import pymongo
from bson import ObjectId

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

pat = "668189b31ebb89530557e7b7"

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
                "$eq": ["$patient_for_today.v._id", ObjectId(pat)]
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

result = plan_for_week.aggregate(pipeline)

print([item for item in result])
print([item for item in plan_for_week.find()])