import pandas as pd
import matplotlib.pyplot as plt

cluster_size = 4
# Load data
sys_name = "vortex"  # or "ray"
plot_name = f"ppl1_{sys_name}_cluster{cluster_size}"



# Color and label configuration
frameworks = ['Torch Serve', 'Ray Monolithic', 'Ray Microservice', 'Vortex Monolithic', 'Vortex Microservice']
colors = ['#444444', '#5B8DB8', '#264E86', '#E57373', '#A61B1B']

plt.figure(figsize=(10, 6))
cur_alpha = 1
cur_markersize = 12
cur_capsize = 6

# # Ray Monolithic
if sys_name == "ray":
    # Ray Monolithic
    ray_df = pd.read_csv(f"ray_cluster{cluster_size}_summary.csv")
    print(ray_df)
    mask = ray_df[['ThroughputMono', 'Latency5Mono', 'LatencyMedMono', 'Latency95Mono']].notna().all(axis=1)
    plt.errorbar(ray_df['ThroughputMono'][mask], ray_df['LatencyMedMono'][mask],
                yerr=[
                    (ray_df['LatencyMedMono'] - ray_df['Latency5Mono'])[mask],
                    (ray_df['Latency95Mono'] - ray_df['LatencyMedMono'])[mask]
                ],
                fmt='-s', markersize=cur_markersize,markeredgewidth=2.5, capsize=cur_capsize,alpha=cur_alpha,
                label='Ray Monolithic', color=colors[1])

    # Ray Microservice
    mask = ray_df[['ThroughputMicro', 'Latency5Micro', 'LatencyMedMicro', 'Latency95Micro']].notna().all(axis=1)
    plt.errorbar(ray_df['ThroughputMicro'][mask], ray_df['LatencyMedMicro'][mask],
                yerr=[
                    (ray_df['LatencyMedMicro'] - ray_df['Latency5Micro'])[mask],
                    (ray_df['Latency95Micro'] - ray_df['LatencyMedMicro'])[mask]
                ],
                fmt='-o', markersize=cur_markersize, markeredgewidth=2.5,capsize=cur_capsize,alpha=cur_alpha,
                label='Ray Microservice', color=colors[2])

# # Vortex Monolithic
if sys_name == "vortex":
    vortex_df = pd.read_csv(f"vortex_cluster{cluster_size}_summary.csv")
    print(vortex_df)
    mask = vortex_df[['ThroughputMono', 'Latency5Mono', 'LatencyMedMono', 'Latency95Mono']].notna().all(axis=1)
    plt.errorbar(vortex_df['ThroughputMono'][mask], vortex_df['LatencyMedMono'][mask],
                yerr=[
                    (vortex_df['LatencyMedMono'] - vortex_df['Latency5Mono'])[mask],
                    (vortex_df['Latency95Mono'] - vortex_df['LatencyMedMono'])[mask]
                ],
                fmt='-s', markersize=cur_markersize, capsize=cur_capsize,alpha=cur_alpha,
                label='Vortex Monolithic', color=colors[3])

    # Vortex Microservice
    mask = vortex_df[['ThroughputMicro', 'Latency5Micro', 'LatencyMedMicro', 'Latency95Micro']].notna().all(axis=1)
    plt.errorbar(vortex_df['ThroughputMicro'][mask], vortex_df['LatencyMedMicro'][mask],
                yerr=[
                    (vortex_df['LatencyMedMicro'] - vortex_df['Latency5Micro'])[mask],
                    (vortex_df['Latency95Micro'] - vortex_df['LatencyMedMicro'])[mask]
                ],
                fmt='-o', markersize=cur_markersize, capsize=cur_capsize,alpha=cur_alpha,
                label='Vortex Microservice', color=colors[4])

# Plot formatting
plt.xlabel('Throughput (queries/sec)', fontsize=26)
plt.ylabel('Latency (ms)', fontsize=26)
plt.title(f"Latency vs Throughput on Cluster{cluster_size}", fontsize=26)
if cluster_size == 7:
    plt.xlim([20, 250])
    plt.ylim([0, 1000])
elif cluster_size == 4:
    plt.xlim([20, 130])
    plt.ylim([0, 1000])
plt.tick_params(axis='both', labelsize=24)
plt.legend(fontsize=24, loc='upper left') 
plt.grid(True)
plt.tight_layout()

# Save and display
plt.savefig(f'{plot_name}_micro_vs_mono.pdf')
plt.show()