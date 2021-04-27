import numpy as np
from numpy.random import default_rng
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from model import EconomiaSocialista

rng = default_rng()

model_params = {
    "I": rng.integers(100, 1000),
    "J": 0, 
    "impuesto_ingreso": np.round(rng.uniform(), 2),
    "costo_vida": rng.integers(0, 100),
    "ingreso_inicial": rng.integers(0, 100)
}

print(model_params)

chart = ChartModule([{"Label": "Gini",
                      "Color": "#18496D"}],
                    data_collector_name='datacollector')

server = ModularServer(EconomiaSocialista, [chart], "Economia Socialista", model_params)
server.port = 8521 # The default
server.launch()