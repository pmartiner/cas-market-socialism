import numpy as np
import inspect
from numpy.random import default_rng
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, BarChartModule
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
        max_value=5000,
        step=50,
        description="Costo de vivir en la economía",
    ),
    "ingreso_inicial": UserSettableParameter(
        "slider",
        name="Ingreso inicial en la economía",
        value=0,
        min_value=0,
        max_value=5000,
        step=50,
        description="Ingreso inicial en la economía",
    )
}

chartGini = ChartModule([{"Label": "Gini",
                      "Color": "#18496D"},],
                    data_collector_name='datacollector')

chartGiniS80S20 = ChartModule([{"Label": "Gini",
                      "Color": "#18496D"},
                      {"Label": "S80/S20",
                      "Color": "#A43DC6"}],
                    data_collector_name='datacollector')

chartConsumidores = ChartModule([{"Label": "Gini",
                      "Color": "#18496D"},
                      {"Label": "S80/S20",
                      "Color": "#A43DC6"},
                      {"Label": "Consumidores",
                      "Color": "#993599"}],
                    data_collector_name='datacollector')

agent_bar = BarChartModule(
    fields=[{"Label": "Ingreso total", "Color": "#4CCE59"}],
    scope="agent",
    sorting="ascending",
    sort_by="ingreso_total",
)



server = ModularServer(EconomiaSocialista, [chartGini, chartGiniS80S20, chartConsumidores, agent_bar], "Economia socialista", model_params)
server.port = 8521 # The default
server.launch()