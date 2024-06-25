import os

import pymongo

from sequenziamento.interface_db import loader_data, convertToHours, save_result, print_result_scheduling
from sequenziamento.model import *

giorno = "Lunedi"
data = loader_data(giorno)
instance = model.create_instance(data)

# Imposta l'indirizzo email NEOS
os.environ['NEOS_EMAIL'] = 'emanuele.rovaretto@edu.unito.it'

# Imposta il solutore su NEOS
# solver_manager = SolverManagerFactory('neos')
solver_manager = SolverFactory('cplex', executable="/opt/ibm/ILOG/CPLEX_Studio128/cplex/bin/x86-64_linux/cplex")
solver_manager.options['timelimit'] = 1

# Risolvi il problema di ottimizzazione
results = solver_manager.solve(instance)

# for v in instance.component_data_objects(Var, active=True):
#     print(v, value(v))

save_result(instance,data,giorno)

print_result_scheduling(giorno)
