import numpy as np
from numpy.random import default_rng
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from model import EconomiaSocialista

rng = default_rng()

model_params = {
    "I": UserSettableParameter(
        "slider",
        name="Número de consumidores",
        value=100,
        min_value=100,
        max_value=1000,
        step=100,
        description="Número de consumidores en la economía",
    ),
    "J": 0, 
    "impuesto_ingreso": UserSettableParameter(
        "slider",
        name="Impuesto al ingreso",
        value=0.2,
        min_value=0,
        max_value=1,
        step=0.05,
        description="Impuesto al ingreso en la economía",
    ),
    "costo_vida": UserSettableParameter(
        "slider",
        name="Costo de vivir en la economía",
        value=10,
        min_value=0,
        max_value=100,
        step=1,
        description="Costo de vivir en la economía",
    ),
    "ingreso_inicial": UserSettableParameter(
        "slider",
        name="Ingreso inicial en la economía",
        value=0,
        min_value=0,
        max_value=1000,
        step=50,
        description="Ingreso inicial en la economía",
    )
}

print(model_params)

chart = ChartModule([{"Label": "Gini",
                      "Color": "#18496D"}],
                    data_collector_name='datacollector')

server = ModularServer(EconomiaSocialista, [chart], "Economia Socialista", model_params)
server.port = 8521 # The default
server.launch()