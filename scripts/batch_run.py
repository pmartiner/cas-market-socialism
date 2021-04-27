import matplotlib.pyplot as plt
import numpy as np
from numpy.random import default_rng
from mesa.batchrunner import BatchRunner

from model import EconomiaSocialista
from model_data_collection import compute_gini

rng = default_rng()

fixed_params = {
    "J": 0,
}

variable_params = {
    "I": range(100, 1000, 100),
    "impuesto_ingreso": np.round(rng.uniform(0, 1, 10), 2),
    "costo_vida": rng.integers(0, 100, 10),
    "ingreso_inicial": rng.integers(0, 100, 10)
}

# The variables parameters will be invoke along with the fixed parameters allowing for either or both to be honored.
# The BatchRunner won’t collect the data every step of the model, but only at the end of each run.
batch_run = BatchRunner(
    EconomiaSocialista,
    variable_params,
    fixed_params,
    iterations=10,
    max_steps=100,
    model_reporters={"Gini": compute_gini}
)

batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
run_data.head()
plt.scatter(run_data.N, run_data.Gini)