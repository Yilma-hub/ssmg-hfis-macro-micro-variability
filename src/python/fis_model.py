import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def build_productivity_system():
    # Inputs
    nitrogen = ctrl.Antecedent(np.arange(4.0, 50.1, 0.1), "nitrogen")
    pH = ctrl.Antecedent(np.arange(5.0, 8.1, 0.1), "pH")
    NDRE = ctrl.Antecedent(np.arange(0.5, 0.91, 0.01), "NDRE")

    # Output
    productivity = ctrl.Consequent(np.arange(0, 18.1, 0.1), "productivity")

    # Membership functions (same as your code)
    nitrogen["low"] = fuzz.trimf(nitrogen.universe, [4.0, 4.0, 15.0])
    nitrogen["medium"] = fuzz.trimf(nitrogen.universe, [4.0, 15.0, 35.0])
    nitrogen["high"] = fuzz.trimf(nitrogen.universe, [15.0, 50.0, 50.0])

    pH["acidic"] = fuzz.trimf(pH.universe, [5.0, 5.0, 6.5])
    pH["neutral"] = fuzz.trimf(pH.universe, [5.0, 6.5, 8.0])
    pH["basic"] = fuzz.trimf(pH.universe, [6.5, 8.0, 8.0])

    NDRE["low"] = fuzz.trimf(NDRE.universe, [0.5, 0.5, 0.7])
    NDRE["medium"] = fuzz.trimf(NDRE.universe, [0.5, 0.7, 0.9])
    NDRE["high"] = fuzz.trimf(NDRE.universe, [0.7, 0.9, 0.9])

    productivity["very low"] = fuzz.trimf(productivity.universe, [0, 0, 4])
    productivity["low"] = fuzz.trimf(productivity.universe, [2, 6, 10])
    productivity["medium"] = fuzz.trimf(productivity.universe, [8, 12, 16])
    productivity["high"] = fuzz.trimf(productivity.universe, [14, 16, 18])
    productivity["very high"] = fuzz.trimf(productivity.universe, [16, 18, 18])

    # Rules (your 27 rules)
    rules = [
        ctrl.Rule(nitrogen["low"] & pH["acidic"] & NDRE["low"], productivity["very low"]),
        ctrl.Rule(nitrogen["low"] & pH["acidic"] & NDRE["medium"], productivity["low"]),
        ctrl.Rule(nitrogen["low"] & pH["acidic"] & NDRE["high"], productivity["low"]),
        ctrl.Rule(nitrogen["low"] & pH["neutral"] & NDRE["low"], productivity["low"]),
        ctrl.Rule(nitrogen["low"] & pH["neutral"] & NDRE["medium"], productivity["medium"]),
        ctrl.Rule(nitrogen["low"] & pH["neutral"] & NDRE["high"], productivity["high"]),
        ctrl.Rule(nitrogen["low"] & pH["basic"] & NDRE["low"], productivity["low"]),
        ctrl.Rule(nitrogen["low"] & pH["basic"] & NDRE["medium"], productivity["high"]),
        ctrl.Rule(nitrogen["low"] & pH["basic"] & NDRE["high"], productivity["very high"]),

        ctrl.Rule(nitrogen["medium"] & pH["acidic"] & NDRE["low"], productivity["very low"]),
        ctrl.Rule(nitrogen["medium"] & pH["acidic"] & NDRE["medium"], productivity["low"]),
        ctrl.Rule(nitrogen["medium"] & pH["acidic"] & NDRE["high"], productivity["medium"]),
        ctrl.Rule(nitrogen["medium"] & pH["neutral"] & NDRE["low"], productivity["low"]),
        ctrl.Rule(nitrogen["medium"] & pH["neutral"] & NDRE["medium"], productivity["medium"]),
        ctrl.Rule(nitrogen["medium"] & pH["neutral"] & NDRE["high"], productivity["high"]),
        ctrl.Rule(nitrogen["medium"] & pH["basic"] & NDRE["low"], productivity["medium"]),
        ctrl.Rule(nitrogen["medium"] & pH["basic"] & NDRE["medium"], productivity["high"]),
        ctrl.Rule(nitrogen["medium"] & pH["basic"] & NDRE["high"], productivity["very high"]),

        ctrl.Rule(nitrogen["high"] & pH["acidic"] & NDRE["low"], productivity["low"]),
        ctrl.Rule(nitrogen["high"] & pH["acidic"] & NDRE["medium"], productivity["medium"]),
        ctrl.Rule(nitrogen["high"] & pH["acidic"] & NDRE["high"], productivity["high"]),
        ctrl.Rule(nitrogen["high"] & pH["neutral"] & NDRE["low"], productivity["medium"]),
        ctrl.Rule(nitrogen["high"] & pH["neutral"] & NDRE["medium"], productivity["high"]),
        ctrl.Rule(nitrogen["high"] & pH["neutral"] & NDRE["high"], productivity["high"]),
        ctrl.Rule(nitrogen["high"] & pH["basic"] & NDRE["low"], productivity["medium"]),
        ctrl.Rule(nitrogen["high"] & pH["basic"] & NDRE["medium"], productivity["high"]),
        ctrl.Rule(nitrogen["high"] & pH["basic"] & NDRE["high"], productivity["very high"]),
    ]

    system = ctrl.ControlSystem(rules)
    sim = ctrl.ControlSystemSimulation(system)
    return sim


def label_productivity(zone_value: float) -> str:
    # same thresholds you used
    if zone_value <= 9.16:
        return "Very Low"
    elif zone_value <= 10.74:
        return "Low"
    elif zone_value <= 12.93:
        return "Medium"
    elif zone_value <= 14.57:
        return "High"
    else:
        return "Very High"


def simulate_observations(nitrogen_obs, ph_obs, ndre_obs, yield_obs=None):
    sim = build_productivity_system()

    zones = []
    labels = []
    for i in range(len(nitrogen_obs)):
        sim.input["nitrogen"] = float(nitrogen_obs[i])
        sim.input["pH"] = float(ph_obs[i])
        sim.input["NDRE"] = float(ndre_obs[i])
        sim.compute()
        z = float(sim.output["productivity"])
        zones.append(z)
        labels.append(label_productivity(z))

    df = pd.DataFrame({
        "nitrogen": nitrogen_obs,
        "pH": ph_obs,
        "NDRE": ndre_obs,
        "Productivity Zone": zones,
        "Productivity Label": labels,
    })

    if yield_obs is not None:
        df.insert(0, "Yield", yield_obs)

    return df
