import os

from sequenziamento.model import *

data = DataPortal()
data.load(filename='data.dat')
instance = model.create_instance(data)

# Imposta l'indirizzo email NEOS
os.environ['NEOS_EMAIL'] = 'emanuele.rovaretto@edu.unito.it'

# Imposta il solutore su NEOS
solver_manager = SolverFactory('cplex', executable="/opt/ibm/ILOG/CPLEX_Studio128/cplex/bin/x86-64_linux/cplex")

#solver_manager = SolverManagerFactory('neos')

# Risolvi il problema di ottimizzazione
results = solver_manager.solve(instance)

# for v in instance.component_data_objects(Var, active=True):
#     print(v, value(v))

sale = {'A': {}, 'B': {}, 'C': {}}

for i in instance.I:
    sale[instance.o[i]][i] = value(instance.c[i])

for s in sale.keys():
    sale[s] = dict(sorted(sale[s].items(),key=lambda x:x[1]))

file = open('data_patient_OUTPUT_1.data','w')
for s in sale.keys():
    file.write("SALA " + s +'\n')
    for i in sale[s].keys():
        file.write(str(sale[s][i]) + ' : ' + i + '\n')
file.write("max BIM: " + str(value(instance.h)))
file.close()

for v in instance.component_data_objects(Var, active=True):
    print(v, value(v))

# param q :=
# (Adolfo, 'Adolfo') 1
# ('Adolfo', 'Alessandro') 0
# ('Adolfo', 'Andrea') 1
# ('Adolfo', 'Antonio') 0
# ('Adolfo', 'Arturo') 1
# ('Alessandro', 'Adolfo') 0
# ('Alessandro', 'Alessandro') 1
# ('Alessandro', 'Andrea') 0
# ('Alessandro', 'Antonio') 1
# ('Alessandro', 'Arturo') 0
# ('Andrea', 'Adolfo') 1
# ('Andrea', 'Alessandro') 0
# ('Andrea', 'Andrea') 1
# ('Andrea', 'Antonio') 0
# ('Andrea', 'Arturo') 1
# ('Antonio', 'Adolfo') 0
# ('Antonio', 'Alessandro') 1
# ('Antonio', 'Andrea') 0
# ('Antonio', 'Antonio') 1
# ('Antonio', 'Arturo') 0
# ('Arturo', 'Adolfo') 1
# ('Arturo', 'Alessandro') 0
# ('Arturo', 'Andrea') 1
# ('Arturo', 'Antonio') 0
# ('Arturo', 'Arturo') 1
# ;

