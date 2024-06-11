import pymongo
import requests
from riak import RiakClient

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

dbOspedale = myclient["ospedale"]

patient_list = dbOspedale["waiting-list"]
patient_list.drop()


def loadRiak():
    url = 'http://172.28.0.3:8098/riak/ospedale1/' + "waiting-list"
    waiting_list = ['B-Ge-i-1-653', 'B-Ge-i-5-063.2', 'B-Ge-i-5-067.0', 'B-Ge-i-5-381.02', 'B-Ge-i-5-381.70',
                    'B-Ge-i-5-393.53', 'B-Ge-i-5-393.54', 'B-Ge-i-5-434.51', 'B-Ge-i-5-445.41', 'B-Ge-i-5-455.41',
                    'B-Ge-i-5-455.71', 'B-Ge-i-5-465.1', 'B-Ge-i-5-469.20', 'B-Ge-i-5-470.10', 'B-Ge-i-5-490.0',
                    'B-Ge-i-5-491.0', 'B-Ge-i-5-491.12', 'B-Ge-i-5-493.5', 'B-Ge-i-5-493.6', 'B-Ge-i-5-511.21',
                    'B-Ge-i-5-524.2', 'B-Ge-i-5-530.31', 'B-Ge-i-5-530.32', 'B-Ge-i-5-530.33', 'B-Ge-i-5-530.71',
                    'B-Ge-i-5-534.03', 'B-Ge-i-5-534.33', 'B-Ge-i-5-534.35', 'B-Ge-i-5-535.31', 'B-Ge-i-5-535.35',
                    'B-Ge-i-5-536.45', 'B-Ge-i-5-536.47', 'B-Ge-i-5-541.0', 'B-Ge-i-5-541.1', 'B-Ge-i-5-794.k6',
                    'B-Ge-i-5-800.4h', 'B-Ge-i-5-820.41', 'B-Ge-i-5-822.g1', 'B-Ge-i-5-865.7', 'B-Ge-i-5-865.8',
                    'B-Ge-i-5-894.06', 'B-Ge-i-5-894.0a', 'B-Ge-i-5-894.1a', 'B-Ge-i-5-895.0c', 'B-Ge-i-5-896.1b',
                    'B-Ge-i-5-896.1f', 'B-Ge-i-5-897.0', 'B-Ge-i-5-897.1', 'B-Ge-i-5-900.1b', 'B-Ge-i-5-916.a0',
                    'B-Ge-i-5-916.a1']
    x = requests.post(url, json=waiting_list)

loadRiak()



#url = 'http://172.28.0.3:8098/riak/ospedale1/' + "waiting-list"
#res = requests.get(url)
#prova = res.json()
#print(prova)


# Crea un'istanza del client di Riak
client = RiakClient(protocol='http', host='172.28.0.3', http_port=8098)

# Ottieni un riferimento al bucket
bucket = client.bucket('ospedale1')

# Ottieni le proprietà del bucket
bucket_props = bucket.get_bucket_props()

# Stampa le proprietà del bucket
print(bucket_props)