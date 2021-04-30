import numpy as np

# Model-level data collection function
def compute_gini(model):
    ingresos_tot = [agent.ingreso_total for agent in model.schedule.agents]
    x = sorted(ingresos_tot)
    N = len(model.schedule.agents)
    acc = 0
    denom = np.mean(x) * N * (N - 1)

    for i in range(N):
        acc += (2*(i + 1) - N -1)*x[i]

    if denom != 0:
        G = np.round(acc / denom, 2)
    else:
        G = 1

    return G

def compute_s80_s20(model):
    ingresos_tot = [agent.ingreso_total for agent in model.schedule.agents]
    s80 = 0
    s20 = 0
    
    if (not np.isnan(np.percentile(ingresos_tot, 80))):
        s80 = np.percentile(ingresos_tot, 80)
    
    if (not np.isnan(np.percentile(ingresos_tot, 20))):
        s20 = np.percentile(ingresos_tot, 20)

    if s20 != 0:
        s80_s20 = np.round(s80 / s20, 2)
    else:
        s80_s20 = 0

    return s80_s20