from pulp import *

# Models and GPUs
models = ['A', 'B', 'C', 'D']
total_gpu = 7
gpus = [f'G{i}' for i in range(total_gpu)]
partition_mem = {'24GB': 24, '12GB': 12, '6GB': 6}


configs = {
    'A': [('BZ1', '24GB'), ('BZ2', '12GB'), ('BZ3', '6GB')],
    'B': [('BZ1', '24GB')],
    'C': [('BZ1', '12GB'), ('BZ2', '12GB'), ('BZ3', '6GB')],
    'D': [('BZ1', '24GB'), ('BZ2', '12GB'), ('BZ3', '6GB')],
}

# Profile: (memory GB, throughput req/s, latency ms)
profile = {
    ('A', 'BZ1', '24GB'): (2.029, 963.85, 14.91),
    ('A', 'BZ2', '12GB'): (0.881, 385.25, 10.07),
    ('A', 'BZ3', '6GB'):  (0.881, 263, 10.07),
    ('B', 'BZ1', '24GB'): (20.919, 45.76, 349.66),
    ('C', 'BZ1', '12GB'): (0.854, 271, 2.0),
    ('C', 'BZ2', '12GB'): (0.854, 271, 2.0),
    ('C', 'BZ3', '6GB'):  (0.854, 271, 2.0),
    ('D', 'BZ1', '24GB'): (0.775, 70, 209.29),
    ('D', 'BZ2', '12GB'): (0.775, 60, 209.29),
    ('D', 'BZ3', '6GB'):  (0.775, 55, 296.93),
}

# ILP setup
prob = LpProblem("Corrected_Shared_MIG_Placement", LpMaximize)

# Replica variables
x = {}
for m in models:
    for g in gpus:
        for bz, mig in configs[m]:
            x[(m, g, bz, mig)] = LpVariable(f"x_{m}_{g}_{bz}_{mig}", lowBound=0, cat=LpInteger)

# Slot variables
co_slot = {g: LpVariable(f"co_slot_{g}", lowBound=0, cat=LpInteger) for g in gpus}
dedicated_6gb = {g: LpVariable(f"dedicated6_{g}", lowBound=0, cat=LpInteger) for g in gpus}
full_24gb = {g: LpVariable(f"full24_{g}", lowBound=0, cat=LpInteger) for g in gpus}

# Throughput target
T = LpVariable("System_Throughput", lowBound=0)
prob += T

# Throughput constraint
for m in models:
    prob += lpSum(x[(m, g, bz, mig)] * profile[(m, bz, mig)][1]
                  for g in gpus for (bz, mig) in configs[m]) >= T

# A + C coexistence: 1 A + 1 C per shared MIG partition
for g in gpus:
    prob += x[('A', g, 'BZ3', '6GB')] <= co_slot[g], f"CoShared_A_Limit_{g}"
    prob += x[('C', g, 'BZ3', '6GB')] <= co_slot[g], f"CoShared_C_Limit_{g}"

# D dedicated 6GB MIGs
for g in gpus:
    prob += x[('D', g, 'BZ3', '6GB')] <= dedicated_6gb[g]

# B uses full 24GB MIG
for g in gpus:
    prob += x[('B', g, 'BZ1', '24GB')] <= full_24gb[g]

# Total memory per GPU ≤ 24GB
for g in gpus:
    prob += (
        co_slot[g] * 6 +
        dedicated_6gb[g] * 6 +
        full_24gb[g] * 24
    ) <= 24

# Solve
prob.solve()

# Output
print("Status:", LpStatus[prob.status])
print("System Throughput:", value(T))
for key, var in x.items():
    if var.varValue and var.varValue > 0:
        print(f"Model {key[0]} on GPU {key[1]} using config ({key[2]}, {key[3]}): {int(var.varValue)} replica(s)")