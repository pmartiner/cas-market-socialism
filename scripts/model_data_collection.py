import numpy as np

# Model-level data collection function
def compute_gini(model):
    ingresos_tot = [agent.ingreso_total for agent in model.schedule.agents]

    if len(ingresos_tot) > 0:
        x = sorted(ingresos_tot)
        N = len(model.schedule.agents)
        acc = 0
        denom = np.nanmean(x) * N * (N - 1)

        for i in range(N):
            acc += (2*(i + 1) - N -1)*x[i]

        if denom != 0:
            G = np.round(acc / denom, 3)
        else:
            G = 1

        return G

def compute_s80_s20(model):
    ingresos_tot = [agent.ingreso_total for agent in model.schedule.agents]

    if len(ingresos_tot) > 0:
        s80 = np.nanpercentile(ingresos_tot, 80)
        s20 = np.nanpercentile(ingresos_tot, 20)

        if s20 != 0:
            s80_s20 = np.round(s80 / s20, 2)
        else:
            s80_s20 = 0

        return s80_s20