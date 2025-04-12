from pulp import *

# ---------------------
# Setup
# ---------------------
total_gpu = 4
models = ['AC', 'B',  'D']
gpus = [f'G{i}' for i in range(total_gpu)]

# Valid configurations per model: (batch_id, MIG_type)
configs = {
    'AC': [('BZ1', '24GB'), ('BZ2', '12GB'), ('BZ3', '6GB')],
    'B': [('BZ1', '24GB')],
    # 'C': [('BZ1', '12GB'), ('BZ2', '12GB'), ('BZ3', '6GB')],
    'D': [('BZ1', '24GB'), ('BZ2', '12GB'), ('BZ3', '6GB')],
}

# Profile: (memory in GB, throughput in req/s, latency in sec)
profile = {
    # ('A', 'BZ1', '24GB'): (2.029, 963.85, 14.91),
    # ('A', 'BZ2', '12GB'): (0.881, 385.25, 10.07),
    # ('A', 'BZ3', '6GB'):  (0.881, 263, 10.07),
    ('AC', 'BZ1', '12GB'): (0.854, 271, 2.0),
    ('AC', 'BZ2', '12GB'): (0.854, 200, 2.0),
    ('AC', 'BZ3', '6GB'):  (0.854, 160, 2.0),
    ('B', 'BZ1', '24GB'): (20.919, 45.76, 349.66),
    ('D', 'BZ1', '24GB'): (0.775, 70, 209.29),
    ('D', 'BZ2', '12GB'): (0.775, 60, 209.29),
    ('D', 'BZ3', '6GB'):  (0.775, 55, 296.93),
}

# ---------------------
# Define the ILP problem
# ---------------------
prob = LpProblem("Maximize_Min_Throughput", LpMaximize)

# ---------------------
# Decision variables
# ---------------------
x = {}
for m in models:
    for g in gpus:
        for bz, mig in configs[m]:
            x[(m, g, bz, mig)] = LpVariable(f"x_{m}_{g}_{bz}_{mig}", lowBound=0, cat=LpInteger)

T = LpVariable("System_Throughput", lowBound=0)

# ---------------------
# Objective
# ---------------------
prob += T, "Maximize_Min_Throughput"

# ---------------------
# Throughput constraints
# ---------------------
for m in models:
    prob += lpSum(
        x[(m, g, bz, mig)] * profile[(m, bz, mig)][1]
        for g in gpus for (bz, mig) in configs[m]
    ) >= T, f"Throughput_{m}"

# ---------------------
# Memory constraint per GPU
# ---------------------
for g in gpus:
    prob += lpSum(
        x[(m, g, bz, mig)] * profile[(m, bz, mig)][0]
        for m in models for (bz, mig) in configs[m]
    ) <= 24, f"Memory_{g}"

# ---------------------
# Solve it
# ---------------------
prob.solve()

# ---------------------
# Output results
# ---------------------
print("Status:", LpStatus[prob.status])
print("System Throughput:", value(T))
print("\nModel assignments:")
for key, var in x.items():
    if var.varValue and var.varValue > 0:
        print(f"Model {key[0]} on GPU {key[1]} using config ({key[2]}, {key[3]}): {int(var.varValue)} replica(s)")
