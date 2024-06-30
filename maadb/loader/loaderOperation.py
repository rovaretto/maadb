import csv
from io import StringIO

import numpy
import pymongo
import requests
from numpy import random


def extractDistribution(loc, specialty, typePatient):
    file = open('main-distribution.csv', 'r')
    righeFile = csv.reader(StringIO(file.read()))
    opcode_data = {}

    for righe in righeFile:
        if righe[0] == loc and righe[1] == specialty and righe[2] == typePatient:
            opcode = righe[3]  # Supponendo che l'opcode sia sempre all'indice 3
            if opcode not in opcode_data:
                opcode_data[opcode] = []
            opcode_data[opcode].append((righe[4], righe[5], righe[6], righe[7]))
    file.close()

    return opcode_data


def calculateDistribution(distribution):
    opcode_distribution = {}
    for op in distribution:
        dist = distribution[op]
        totalTime = 0
        for elem in dist:
            if elem[1] == 'lognormal':
                mean = float(elem[2].replace(",", "."))
                sigma = float(elem[3].replace(",", "."))
                tmp = random.lognormal(mean=mean, sigma=sigma)
                totalTime = totalTime + tmp
            elif elem[1] == 'weibull':
                shape = float(elem[2].replace(",", "."))
                scala = float(elem[3].replace(",", "."))
                tmp = scala * random.weibull(a=shape)
                totalTime = totalTime + tmp
            elif elem[1] == 'gamma':
                shape = float(elem[2].replace(",", "."))
                scala = float(elem[3].replace(",", "."))
                tmp = random.gamma(shape=shape, scale=scala)
                totalTime = totalTime + tmp

        opcode_distribution[op] = numpy.ceil(totalTime)
    return opcode_distribution


#genera pazienti di tutte le specialità
def generateAllPatient():
    distribution = {}
    for loc in ['Basic & Regular', 'Maximum excl. University Clinics', 'Specialized']:
        for speciality in ['General', 'Gyn & Obstetrics', 'Otolaryngology', 'Trauma']:
            for typePatient in ['inpatient', 'outpatient']:
                distribution[loc, speciality, typePatient] = calculateDistribution(
                    extractDistribution(loc, speciality, typePatient))

    return distribution


def generateOperationWithDuration():
    distribution = generateAllPatient()
    result = {}
    for patKey in distribution.keys():
        for opCode in distribution[patKey]:
            key = hashing(patKey, opCode)
            result[key] = distribution[patKey][opCode]
    return result


def hashing(key, opcode):
    return key[0][0] + "-" + key[1][0] + key[1][1] + "-" + key[2][0] + "-" + opcode


def loadOperation():
    opcode_duration = generateOperationWithDuration()
    duration_op.drop()
    for opcode in opcode_duration:
        agg = {'opcode': opcode, 'duration': opcode_duration[opcode]}
        duration_op.insert_one(agg)

def getDuration(opcode):
    result = duration_op.find_one({'op':opcode})
    return result['duration']

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
dbOspedale = myclient["ospedale"]
duration_op = dbOspedale["duration-op"]

loadOperation()

# print(getDuration('S-Tr-o-5-841.14'))