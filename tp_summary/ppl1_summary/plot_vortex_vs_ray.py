import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams.update({
    "text.usetex": False,
    "font.family": "serif",
    "font.serif": ["Computer Modern", "Latin Modern Roman", "CMU Serif", "DejaVu Serif"],
    "pdf.fonttype": 42,
    "ps.fonttype": 42
})

from plot_colors import frame_colors

cluster_size = 4
# Load data
sys_name = "ray"  # or "ray"
plot_name = f"ppl1_vr_cluster{cluster_size}"



# Color and label configuration
frameworks = ['Torch Serve', 'Ray Monolithic', 'Ray Microservice', 'Vortex Monolithic', 'Vortex Microservice']
colors = ['#444444', '#5B8DB8', '#264E86', '#E57373', '#A61B1B']

plt.figure(figsize=(10.5, 5))
cur_alpha = 1
cur_markersize = 12
cur_capsize = 6

# # Ray Monolithic
# Ray Monolithic
ray_df = pd.read_csv(f"ray_cluster{cluster_size}_summary.csv")
# print(ray_df)
mask = ray_df[['ThroughputMono', 'Latency5Mono', 'LatencyMedMono', 'Latency95Mono']].notna().all(axis=1)
# plt.errorbar(ray_df['ThroughputMono'][mask], ray_df['LatencyMedMono'][mask],
#             yerr=[
#                 (ray_df['LatencyMedMono'] - ray_df['Latency5Mono'])[mask],
#                 (ray_df['Latency95Mono'] - ray_df['LatencyMedMono'])[mask]
#             ],
#             fmt='-s', markersize=cur_markersize,markeredgewidth=2.5, capsize=cur_capsize,alpha=cur_alpha,
#             linestyle='--',label='Ray Monolithic', color=frame_colors['Ray Monolithic'])

# Ray Microservice
mask = ray_df[['ThroughputMicro', 'Latency5Micro', 'LatencyMedMicro', 'Latency95Micro']].notna().all(axis=1)
plt.errorbar(ray_df['ThroughputMicro'][mask], ray_df['LatencyMedMicro'][mask],
            yerr=[
                (ray_df['LatencyMedMicro'] - ray_df['Latency5Micro'])[mask],
                (ray_df['Latency95Micro'] - ray_df['LatencyMedMicro'])[mask]
            ],
            fmt='-o', markersize=cur_markersize, markeredgewidth=2.5,capsize=cur_capsize,alpha=cur_alpha,
            label='Ray', color=frame_colors['Ray Microservice'])

# # Vortex Monolithic

vortex_df = pd.read_csv(f"vortex_cluster{cluster_size}_summary.csv")
# print(vortex_df)
mask = vortex_df[['ThroughputMono', 'Latency5Mono', 'LatencyMedMono', 'Latency95Mono']].notna().all(axis=1)
# plt.errorbar(vortex_df['ThroughputMono'][mask], vortex_df['LatencyMedMono'][mask],
#             yerr=[
#                 (vortex_df['LatencyMedMono'] - vortex_df['Latency5Mono'])[mask],
#                 (vortex_df['Latency95Mono'] - vortex_df['LatencyMedMono'])[mask]
#             ],
#             fmt='-s', markersize=cur_markersize, capsize=cur_capsize,alpha=cur_alpha,
#             linestyle='--',label='Vortex Monolithic', color=frame_colors['Vortex Monolithic'])

# Vortex Microservice
mask = vortex_df[['ThroughputMicro', 'Latency5Micro', 'LatencyMedMicro', 'Latency95Micro']].notna().all(axis=1)
plt.errorbar(vortex_df['ThroughputMicro'][mask], vortex_df['LatencyMedMicro'][mask],
            yerr=[
                (vortex_df['LatencyMedMicro'] - vortex_df['Latency5Micro'])[mask],
                (vortex_df['Latency95Micro'] - vortex_df['LatencyMedMicro'])[mask]
            ],
            fmt='-o', markersize=cur_markersize, capsize=cur_capsize,alpha=cur_alpha,
            label='Typhoon', color=frame_colors['Vortex Microservice'])
# plt.title(f"Latency vs Throughput of PreFLMR on Cluster{cluster_size}", fontsize=26, pad=10)

# Plot formatting
plt.xlabel('Throughput (queries/sec)', fontsize=27)
plt.ylabel('Latency (ms)', fontsize=27)

if cluster_size == 7:
    plt.xlim([20, 230])
    plt.ylim([0, 1350])
elif cluster_size == 4:
    plt.xlim([20, 120])
    plt.ylim([0, 1350])
plt.tick_params(axis='both', labelsize=25)
plt.legend(fontsize=24, loc='upper left') 
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Save and display
plt.savefig(f'{plot_name}_two.pdf')
print(f'Saved figure to {plot_name}_two.pdf')
plt.show()