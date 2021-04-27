import numpy as np

# Model-level data collection function
def compute_gini(model):
    ingresos_tot = [agent.ingreso_total for agent in model.schedule.agents]
    x = sorted(ingresos_tot)
    N = len(model.schedule.agents)
    acc = 0

    for i in range(N):
        acc += (2*(i + 1) - N -1)*x[i]
    G = np.round(acc / (np.mean(x) * N * (N - 1)), 2)

    return G