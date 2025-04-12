from ortools.linear_solver import pywraplp

# === INPUT DATA ===
models = ['AC', 'B', 'D']
gpus = list(range(4))  # 4 GPUs
mig_configs = [6, 12, 24]

# Throughput of each model on each MIG config (no batching)
throughput = {
    'AC': {6: 200, 12: 240, 24: 270},
    'B': {24: 45},
    'D': {6: 55, 12: 60, 24: 70},
}

# Valid MIG layouts for 24GB GPU (each layout is a list of MIG sizes)
valid_mig_layouts = [
    [24],
    [12, 12],
    [12, 6, 6],
    [6, 6, 6, 6],
]

# === BUILD MIG INSTANCES ===
mig_instances = []  # List of tuples: (gpu_id, mig_size, local_instance_id)
for gpu_id in gpus:
    layout = valid_mig_layouts[gpu_id % len(valid_mig_layouts)]  # Use layout round-robin
    for local_id, size in enumerate(layout):
        mig_instances.append((gpu_id, size, local_id))

# === ILP SETUP ===
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables: x[m][g][c][i] = 1 if model m assigned to MIG inst i of size c on GPU g
x = {}
for m in models:
    for (g, c, i) in mig_instances:
        if c in throughput[m]:
            x[m, g, c, i] = solver.IntVar(0, 1, f'x_{m}_{g}_{c}_{i}')

# Each MIG instance can run at most one model
for (g, c, i) in mig_instances:
    solver.Add(
        sum(x[m, g, c, i] for m in models if (m, g, c, i) in x) <= 1
    )

# Maximize minimum model throughput
z = solver.NumVar(0, solver.infinity(), 'z')
for m in models:
    solver.Add(
        sum(x[m, g, c, i] * throughput[m][c]
            for (g, c, i) in mig_instances if (m, g, c, i) in x) >= z
    )

# Add soft upper bound to avoid skewed assignments (allow at most z + epsilon)
EPSILON = 30
for m in models:
    solver.Add(
        sum(x[m, g, c, i] * throughput[m][c]
            for (g, c, i) in mig_instances if (m, g, c, i) in x) <= z + EPSILON
    )

solver.Maximize(z)

# === SOLVE ===
status = solver.Solve()

# === OUTPUT ===
if status == pywraplp.Solver.OPTIMAL:
    print(f"Optimal minimum throughput: {z.solution_value():.2f}\n")
    for m in models:
        for (g, c, i) in mig_instances:
            if (m, g, c, i) in x and x[m, g, c, i].solution_value() > 0.5:
                print(f"Model {m} assigned to GPU {g}, MIG {c}GB (instance {i})")
else:
    print("No optimal solution found.")
