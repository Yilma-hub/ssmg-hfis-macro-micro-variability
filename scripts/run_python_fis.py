# scripts/run_python_fis.py
import os
import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO_ROOT, "results")
os.makedirs(OUT_DIR, exist_ok=True)

# --- Define variables ---
nitrogen = ctrl.Antecedent(np.arange(4.0, 50.1, 0.1), 'nitrogen')
pH = ctrl.Antecedent(np.arange(5.0, 8.1, 0.1), 'pH')
NDRE = ctrl.Antecedent(np.arange(0.5, 0.91, 0.01), 'NDRE')
productivity = ctrl.Consequent(np.arange(0, 18.1, 0.1), 'productivity')

# --- Membership functions ---
nitrogen['low'] = fuzz.trimf(nitrogen.universe, [4.0, 4.0, 15.0])
nitrogen['medium'] = fuzz.trimf(nitrogen.universe, [4.0, 15.0, 35.0])
nitrogen['high'] = fuzz.trimf(nitrogen.universe, [15.0, 50.0, 50.0])

pH['acidic'] = fuzz.trimf(pH.universe, [5.0, 5.0, 6.5])
pH['neutral'] = fuzz.trimf(pH.universe, [5.0, 6.5, 8.0])
pH['basic'] = fuzz.trimf(pH.universe, [6.5, 8.0, 8.0])

NDRE['low'] = fuzz.trimf(NDRE.universe, [0.5, 0.5, 0.7])
NDRE['medium'] = fuzz.trimf(NDRE.universe, [0.5, 0.7, 0.9])
NDRE['high'] = fuzz.trimf(NDRE.universe, [0.7, 0.9, 0.9])

productivity['very low'] = fuzz.trimf(productivity.universe, [0, 0, 4])
productivity['low'] = fuzz.trimf(productivity.universe, [2, 6, 10])
productivity['medium'] = fuzz.trimf(productivity.universe, [8, 12, 16])
productivity['high'] = fuzz.trimf(productivity.universe, [14, 16, 18])
productivity['very high'] = fuzz.trimf(productivity.universe, [16, 18, 18])

# --- Rules (add all your rules here) ---
rule1 = ctrl.Rule(nitrogen['low'] & pH['acidic'] & NDRE['low'], productivity['very low'])
rule2 = ctrl.Rule(nitrogen['low'] & pH['acidic'] & NDRE['medium'], productivity['low'])
rule3 = ctrl.Rule(nitrogen['low'] & pH['acidic'] & NDRE['high'], productivity['low'])
# ... continue adding rule4..rule27 as in your script ...

system = ctrl.ControlSystem([rule1, rule2, rule3])  # include all rules here
sim = ctrl.ControlSystemSimulation(system)

# --- Observations (replace with your full lists) ---
nitrogen_observation = [6, 11.8, 10.9]
pH_observation = [7.6, 6.8, 7.7]
NDRE_observation = [0.639306, 0.535043, 0.541024]
yield_observation = [8.762764, 4.946119, 6.485314]

zones = []
labels = []

for i in range(len(nitrogen_observation)):
    sim.input['nitrogen'] = nitrogen_observation[i]
    sim.input['pH'] = pH_observation[i]
    sim.input['NDRE'] = NDRE_observation[i]
    sim.compute()

    z = sim.output['productivity']
    zones.append(z)

    if z <= 9.16:
        labels.append('Very Low')
    elif z <= 10.74:
        labels.append('Low')
    elif z <= 12.93:
        labels.append('Medium')
    elif z <= 14.57:
        labels.append('High')
    else:
        labels.append('Very High')

df = pd.DataFrame({
    "Yield": yield_observation,
    "Productivity Zone": zones,
    "Productivity Label": labels
})

out_file = os.path.join(OUT_DIR, "productivity_clusters.xlsx")
df.to_excel(out_file, index=False)
print(f"Saved: {out_file}")
