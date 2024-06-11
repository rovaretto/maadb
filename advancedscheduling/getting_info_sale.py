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

def getDurata():
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
    print(resultDB["results"])
    result = {}
    for elem in resultDB["results"]:
        tupla = elem['_id']
        result[tupla[0],tupla[1], tupla[2]] = 1
        for spec in J:
            if spec != tupla[2]:
                result[tupla[0], tupla[1], spec] = 0

    return result

#I
K = infoSale.distinct("nome")
T = infoSale.distinct("giorniApertura")
J = getSpecialita()

#p
s = getDurata()
#q
tau = getTau(J)

print(tau)