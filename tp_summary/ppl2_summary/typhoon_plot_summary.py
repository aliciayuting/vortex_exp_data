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
sys_name = "Typhoon"
plot_name = f"ppl2_{sys_name}_cluster{cluster_size}"



# Color and label configuration
frameworks = ['Torch Serve', 'Ray Monolithic', 'Ray Microservice', 'Typhoon Monolithic', 'Typhoon Microservice']
colors = ['#444444', '#5B8DB8', '#264E86', '#E57373', '#A61B1B']

plt.figure(figsize=(10, 6))
cur_alpha = 1
cur_markersize = 12
cur_capsize = 6

# # Ray Monolithic
if sys_name == "ray":
    # Ray Monolithic
    ray_df = pd.read_csv(f"ray_cluster{cluster_size}_summary.csv")
    
    mask = ray_df[['ThroughputMono', 'Latency5Mono', 'LatencyMedMono', 'Latency95Mono']].notna().all(axis=1)
    plt.errorbar(ray_df['ThroughputMono'][mask], ray_df['LatencyMedMono'][mask],
                yerr=[
                    (ray_df['LatencyMedMono'] - ray_df['Latency5Mono'])[mask],
                    (ray_df['Latency95Mono'] - ray_df['LatencyMedMono'])[mask]
                ],
                fmt='-s', markersize=cur_markersize,markeredgewidth=2.5, capsize=cur_capsize,alpha=cur_alpha,
                label='Ray Monolithic', color=frame_colors['Ray Monolithic'])

    # Ray Microservice
    mask = ray_df[['ThroughputMicro', 'Latency5Micro', 'LatencyMedMicro', 'Latency95Micro']].notna().all(axis=1)
    plt.errorbar(ray_df['ThroughputMicro'][mask], ray_df['LatencyMedMicro'][mask],
                yerr=[
                    (ray_df['LatencyMedMicro'] - ray_df['Latency5Micro'])[mask],
                    (ray_df['Latency95Micro'] - ray_df['LatencyMedMicro'])[mask]
                ],
                fmt='-o', markersize=cur_markersize, markeredgewidth=2.5,capsize=cur_capsize,alpha=cur_alpha,
                label='Ray Microservice', color=frame_colors['Ray Microservice'])
    plt.title(f"Latency vs Throughput on Ray Cluster{cluster_size}", fontsize=26, pad=10)

# # Typhoon Monolithic
if sys_name == "Typhoon":
    Typhoon_df = pd.read_csv(f"vortex_cluster{cluster_size}_summary.csv")
    print(Typhoon_df)
    mask = Typhoon_df[['ThroughputMono', 'Latency5Mono', 'LatencyMedMono', 'Latency95Mono']].notna().all(axis=1)
    plt.errorbar(Typhoon_df['ThroughputMono'][mask], Typhoon_df['LatencyMedMono'][mask],
                yerr=[
                    (Typhoon_df['LatencyMedMono'] - Typhoon_df['Latency5Mono'])[mask],
                    (Typhoon_df['Latency95Mono'] - Typhoon_df['LatencyMedMono'])[mask]
                ],
                fmt='-s', markersize=cur_markersize, capsize=cur_capsize,alpha=cur_alpha,
                label='Typhoon Monolithic', color=frame_colors['Vortex Monolithic'])

    # Typhoon Microservice
    mask = Typhoon_df[['ThroughputMicro', 'Latency5Micro', 'LatencyMedMicro', 'Latency95Micro']].notna().all(axis=1)
    plt.errorbar(Typhoon_df['ThroughputMicro'][mask], Typhoon_df['LatencyMedMicro'][mask],
                yerr=[
                    (Typhoon_df['LatencyMedMicro'] - Typhoon_df['Latency5Micro'])[mask],
                    (Typhoon_df['Latency95Micro'] - Typhoon_df['LatencyMedMicro'])[mask]
                ],
                fmt='-o', markersize=cur_markersize, capsize=cur_capsize,alpha=cur_alpha,
                label='Typhoon Microservice', color=frame_colors['Vortex Microservice'])
    plt.title(f"Latency vs Throughput on Typhoon Cluster{cluster_size}", fontsize=26, pad=10)

# Plot formatting
plt.xlabel('Throughput (queries/sec)', fontsize=27)
plt.ylabel('Latency (ms)', fontsize=27)

if cluster_size == 4:
    plt.xlim([0, 25])
elif cluster_size == 7:
    plt.xlim([0, 50])
plt.ylim([0, 2000])
plt.tick_params(axis='both', labelsize=25)
plt.legend(fontsize=24, loc='upper left') 
plt.grid(True)
plt.tight_layout()

# Save and display
plt.savefig(f'{plot_name}_micro_vs_mono.pdf')
plt.show()