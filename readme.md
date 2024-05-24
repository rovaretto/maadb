1 installare pyomo - pip install pyomo

2 loggare su neos 

3 Risolvere
 # Imposta l'indirizzo email NEOS
os.environ['NEOS_EMAIL'] = 'emanuele.rovaretto@edu.unito.it'

# Imposta il solutore su NEOS
solver_manager = pe.SolverManagerFactory('neos')


# Risolvi il problema di ottimizzazione
results = solver_manager.solve(model, solver="minos", load_solutions=False)

