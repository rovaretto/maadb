import datetime
import json
import locale
import pymongo
import requests
from bson import json_util

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
dbOspedale = myclient["ospedale"]
plan_for_week = dbOspedale["plan-for-week"]

urlRiak = 'http://localhost:8098/riak/'


def giorno_di_oggi():
    locale.setlocale(locale.LC_TIME, 'it_IT.utf8')
    oggi = datetime.datetime.now()
    return oggi.strftime('%A').capitalize().replace('ì', 'i')
def load_today_data():
    giorno = giorno_di_oggi()
    url = urlRiak + "ospedale1/" + "today"
    print(url)
    today_op = plan_for_week.find_one({'giorno' : giorno})
    today_op_json = json.dumps(today_op, default=json_util.default)
    r = requests.post(url, data=today_op_json, headers={'Content-Type': 'application/json'})
    print(r)

def read_today_data():
    url = urlRiak + "ospedale1/" + "today"
    r = requests.get(url)
    return r.json()

load_today_data()
print(read_today_data())