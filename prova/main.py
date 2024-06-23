import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

dbOspedale = myclient["ospedale"]

infoSale = dbOspedale["info-sale"]
patient_list = dbOspedale["waiting-list"]

print(infoSale.find_one({'nome': 'D'},{"patientPerDay":1}))