import csv
from io import StringIO

import numpy
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


def caluclateDistribution(distribution):
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
                distribution[loc, speciality, typePatient] = caluclateDistribution(
                    extractDistribution(loc, speciality, typePatient))

    return distribution

#genera pazienti con il minutaggio massimo per ogni specialità
def generatePatientMaxMin():
    distribution = generateAllPatient()
    result = {}
    for patKey in distribution.keys():
        for opCode in distribution[patKey]:
            key = hashing(patKey, opCode)
            result[key] = distribution[patKey][opCode]
    return result

def hashing(key,opcode):
    return key[0][0] + "-" + key[1][0] + key[1][1] + "-" + key[2][0] + "-" + opcode

def loadRiak():
    a = generatePatientMaxMin()
    sum=0
    for key in a:
        url = 'http://172.30.0.2:8098/riak/patients/' + key
        myobj = {'duration': a[key]}
        x = requests.post(url, json=myobj)


loadRiak()
