import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

dbOspedale = myclient["ospedale"]

infoSale = dbOspedale["info-sale"]

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


K = infoSale.distinct("nome")
T = infoSale.distinct("giorniApertura")
J = getSpecialita()


print(J)