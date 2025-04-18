import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from plot_colors import frame_colors

mpl.rcParams.update({
    "text.usetex": False,
    "font.family": "serif",
    "font.serif": ["Computer Modern", "Latin Modern Roman", "CMU Serif", "DejaVu Serif"],
    "pdf.fonttype": 42,
    "ps.fonttype": 42
})

# Plotting setup
cluster_size = 4
plot_name = f"ppl1_micro_cluster{cluster_size}"
# Color and label configuration
frameworks = ['Torch Serve', 'Ray Monolithic', 'Ray Microservice', 'Vortex Monolithic', 'Vortex Microservice']

plt.figure(figsize=(12, 6))
cur_alpha = 1
cur_markersize = 12
cur_capsize = 6

# === Ray Microservice ===
ray_df = pd.read_csv(f"ray_cluster{cluster_size}_summary.csv")
mask = ray_df[['ThroughputMicro', 'Latency5Micro', 'LatencyMedMicro', 'Latency95Micro']].notna().all(axis=1)
plt.errorbar(ray_df['ThroughputMicro'][mask], ray_df['LatencyMedMicro'][mask],
             yerr=[
                 (ray_df['LatencyMedMicro'] - ray_df['Latency5Micro'])[mask],
                 (ray_df['Latency95Micro'] - ray_df['LatencyMedMicro'])[mask]
             ],
             fmt='-o', markersize=cur_markersize, capsize=cur_capsize, alpha=cur_alpha,
             label='Ray Microservice', color=frame_colors['Ray Microservice'], markeredgewidth=2.5)

# === Vortex Microservice (TCP) ===
vortex_tcp_df = pd.read_csv(f"vortex_cluster{cluster_size}_summary_tcp.csv")
mask = vortex_tcp_df[['ThroughputMicro', 'Latency5Micro', 'LatencyMedMicro', 'Latency95Micro']].notna().all(axis=1)
plt.errorbar(vortex_tcp_df['ThroughputMicro'][mask], vortex_tcp_df['LatencyMedMicro'][mask],
             yerr=[
                 (vortex_tcp_df['LatencyMedMicro'] - vortex_tcp_df['Latency5Micro'])[mask],
                 (vortex_tcp_df['Latency95Micro'] - vortex_tcp_df['LatencyMedMicro'])[mask]
             ],
             fmt='-o', markersize=cur_markersize, capsize=cur_capsize, alpha=cur_alpha,
             label='Vortex Microservice (TCP)', color=frame_colors['Vortex Microservice (TCP)'], markeredgewidth=2.5)

# === Vortex Microservice (RDMA) ===
vortex_rdma_df = pd.read_csv(f"vortex_cluster{cluster_size}_summary_rdma.csv")
mask = vortex_rdma_df[['ThroughputMicro', 'Latency5Micro', 'LatencyMedMicro', 'Latency95Micro']].notna().all(axis=1)
plt.errorbar(vortex_rdma_df['ThroughputMicro'][mask], vortex_rdma_df['LatencyMedMicro'][mask],
             yerr=[
                 (vortex_rdma_df['LatencyMedMicro'] - vortex_rdma_df['Latency5Micro'])[mask],
                 (vortex_rdma_df['Latency95Micro'] - vortex_rdma_df['LatencyMedMicro'])[mask]
             ],
             fmt='-o', markersize=cur_markersize, capsize=cur_capsize, alpha=cur_alpha,
             label='Vortex Microservice (RDMA)', color=frame_colors['Vortex Microservice'], markeredgewidth=2.5)

# Formatting
plt.title(f"Latency vs Throughput (TCP vs. RDMA)", fontsize=26, pad=10)
plt.xlabel('Throughput (queries/sec)', fontsize=27)
plt.ylabel('Latency (ms)', fontsize=27)
plt.xlim([20, 130])
plt.ylim([0, 1000])
plt.tick_params(axis='both', labelsize=25)
plt.legend(fontsize=22, loc='upper left')
plt.grid(True)
plt.tight_layout()

# Save and display
plt.savefig(f'rdma_vs_tcp_vs_ray_{plot_name}.pdf')
plt.show()