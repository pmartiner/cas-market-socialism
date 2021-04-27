import matplotlib.pyplot as plt
import numpy as np
from numpy.random import default_rng

from model import EconomiaSocialista

ingresos_totales = []
rng = default_rng()

for j in range(50):
    model_params = {
        "I": rng.integers(100, 1000),
        "J": 0, 
        "impuesto_ingreso": np.round(rng.uniform(), 2),
        "costo_vida": rng.integers(0, 100),
        "ingreso_inicial": rng.integers(0, 100)
    }

    print('Corriendo: Modelo #', j)
    print('Params:', model_params)
    
    model = EconomiaSocialista(
        model_params['I'],
        model_params['J'],
        model_params['impuesto_ingreso'],
        model_params['costo_vida'],
        model_params['ingreso_inicial']
    )

    for i in range(100):
        model.step()

    # Store the results
    for agent in model.schedule.agents:
        ingresos_totales.append(agent.ingreso_total)
    
    gini = model.datacollector.get_model_vars_dataframe()
    gini.plot()
    plt.show()

plt.xlabel('Ingreso total')
plt.ylabel('# de consumidores')
plt.title('Ingresos totales acumulados por agentes')
plt.hist(ingresos_totales, bins=range(int(max(ingresos_totales))+1))
plt.show()