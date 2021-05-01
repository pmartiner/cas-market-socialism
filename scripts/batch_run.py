import matplotlib.pyplot as plt
import numpy as np
from numpy.random import default_rng
from mesa.batchrunner import BatchRunner

from model import EconomiaSocialista
from model_data_collection import *

rng = default_rng()

fixed_params = {
    "J": 1,
    "I": 100,
}

variable_params = {
    "impuesto_ingreso": np.round(rng.uniform(0, 1, 10), 2),
    "costo_vida": rng.integers(30, 500, 10),
    "ingreso_inicial": rng.integers(0, 1000, 10)
}

model_reporters={
   "Gini": compute_gini,
   "S80/S20": compute_s80_s20
}

agent_reporters={
    "Ingreso total": "ingreso_total"
}

# The variables parameters will be invoke along with the fixed parameters allowing for either or both to be honored.
# The BatchRunner won’t collect the data every step of the model, but only at the end of each run.
batch_run = BatchRunner(
    EconomiaSocialista,
    variable_params,
    fixed_params,
    iterations=5,
    max_steps=100,
    model_reporters=model_reporters,
    agent_reporters=agent_reporters
)

batch_run.run_all()

run_model_data = batch_run.get_model_vars_dataframe()

# Gini
plt.title('Coeficiente de Gini por iteración')
plt.ylabel('Coeficiente de Gini')
plt.xlabel('Iteración')
plt.scatter(run_model_data.Run, run_model_data.Gini)
plt.show()

plt.title('Coeficiente de Gini ante cambios en el ingreso inicial')
plt.ylabel('Coeficiente de Gini')
plt.xlabel('Ingreso inicial')
plt.scatter(run_model_data.ingreso_inicial, run_model_data.Gini)
plt.show()

plt.title('Coeficiente de Gini ante cambios en el costo de vida')
plt.ylabel('Coeficiente de Gini')
plt.xlabel('Costo de vida')
plt.scatter(run_model_data.costo_vida, run_model_data.Gini)
plt.show()

plt.title('Coeficiente de Gini ante cambios en el impuesto al ingreso')
plt.ylabel('Coeficiente de Gini')
plt.xlabel('Impuesto al ingreso')
plt.scatter(run_model_data.impuesto_ingreso, run_model_data.Gini)
plt.show()

# S80/S20
plt.title('Índice S80/S20 por iteración')
plt.ylabel('Índice S80/S20')
plt.xlabel('Iteración')
plt.scatter(run_model_data.Run, run_model_data["S80/S20"])
plt.show()

plt.title('Índice S80/S20 ante cambios en el ingreso inicial')
plt.ylabel('Índice S80/S20')
plt.xlabel('Ingreso inicial')
plt.scatter(run_model_data.ingreso_inicial, run_model_data["S80/S20"])
plt.show()

plt.title('Índice S80/S20 ante cambios en el costo de vida')
plt.ylabel('Índice S80/S20')
plt.xlabel('Costo de vida')
plt.scatter(run_model_data.costo_vida, run_model_data["S80/S20"])
plt.show()

plt.title('Índice S80/S20 ante cambios en el impuesto al ingreso')
plt.ylabel('Índice S80/S20')
plt.xlabel('Impuesto al ingreso')
plt.scatter(run_model_data.impuesto_ingreso, run_model_data["S80/S20"])
plt.show()

run_agent_data = batch_run.get_agent_vars_dataframe()

plt.title('Distribución de los ingresos a lo largo del tiempo')
plt.xlabel('Iteración')
plt.ylabel('Distribución de los ingresos')
plt.scatter(run_agent_data.Run, run_agent_data["Ingreso total"])
plt.show()