from sequenziamento.interface_db import loader_data, save_result, print_result_scheduling
from sequenziamento.model import *

giorno = "Lunedi"
data = loader_data(giorno)
instance = model.create_instance(data)
solver_manager = SolverFactory('cplex', executable="/opt/ibm/ILOG/CPLEX_Studio128/cplex/bin/x86-64_linux/cplex")
solver_manager.options['timelimit'] = 1
# Risolvi il problema di ottimizzazione
results = solver_manager.solve(instance)
# risolvi
save_result(instance, data, giorno)

print_result_scheduling(giorno)
