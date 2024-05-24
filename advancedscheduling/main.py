import os

from advancedscheduling.model import *

data = DataPortal()
data.load(filename="data_patient.dat")
print(data["I"])
{"I":['B-Ge-i-5-916.a5', 'M-Ge-i-5-987.0']}
#
# instance = model.create_instance(data)
#
# # Imposta l'indirizzo email NEOS
# os.environ['NEOS_EMAIL'] = 'emanuele.rovaretto@edu.unito.it'
#
#
# # Imposta il solutore su NEOS
# solver_manager = SolverManagerFactory('neos')
#
# # Risolvi il problema di ottimizzazione
# results = solver_manager.solve(instance, solver="cplex", load_solutions=True)
#
# file = open('data_patient_OUTPUT', 'w')
# for t in instance.T:
#     for k in instance.K:
#         for i in instance.I:
#             if instance.x[i,k,t].value == 1:
#                 file.write(t + " " + k + " " + i + " " + str(instance.p[i]) + "\n")
#     file.write("---------------------------\n")
# print(results)


# TT =