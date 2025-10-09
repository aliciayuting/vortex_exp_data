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
plot_name = f"ppl1_vr_cluster{cluster_size}_slo"

plt.figure(figsize=(10.5, 5))
cur_markersize = 10
cur_alpha = 1.0
linewidth = 2.5

def plot_slo_lines(df: pd.DataFrame,
                   sys_label: str,
                   color_micro: str,
                   color_mono: str):
    """
    Plot SLO200 and SLO500 for Micro and Mono if present.
    Expects columns:
      - ThroughputMicro, SLO200Micro, SLO500Micro
      - ThroughputMono,  SLO200Mono,  SLO500Mono (optional)
    """

    # --- Microservice ---
    if set(["ThroughputMicro", "SLO200Micro", "SLO500Micro"]).issubset(df.columns):
        msk = df[["ThroughputMicro", "SLO200Micro", "SLO500Micro"]].notna().all(axis=1)
        if msk.any():
            # SLO200
            plt.plot(df.loc[msk, "ThroughputMicro"],
                     df.loc[msk, "SLO200Micro"],
                     marker="o", linestyle="-", linewidth=linewidth,
                     markersize=cur_markersize, alpha=cur_alpha,
                     label=f"{sys_label} (200 ms SLO)",
                     color=color_micro)
            # SLO500 (dash-dot)
            plt.plot(df.loc[msk, "ThroughputMicro"],
                     df.loc[msk, "SLO500Micro"],
                     marker="^", linestyle="--", linewidth=linewidth,
                     markersize=cur_markersize, alpha=cur_alpha,
                     label=f"{sys_label} (500 ms SLO)",
                     color=color_micro)

    # # --- Monolithic (optional) ---
    # want = {"ThroughputMono", "SLO200Mono", "SLO500Mono"}
    # have = want.intersection(df.columns)
    # if len(have) == len(want):
    #     msk = df[["ThroughputMono", "SLO200Mono", "SLO500Mono"]].notna().all(axis=1)
    #     if msk.any():
    #         # SLO200
    #         plt.plot(df.loc[msk, "ThroughputMono"],
    #                  df.loc[msk, "SLO200Mono"],
    #                  marker="s", linestyle="-.", linewidth=linewidth,
    #                  markersize=cur_markersize, alpha=cur_alpha,
    #                  label=f"{sys_label} Mono SLO200",
    #                  color=color_mono)
    #         # SLO500
    #         plt.plot(df.loc[msk, "ThroughputMono"],
    #                  df.loc[msk, "SLO500Mono"],
    #                  marker="v", linestyle=":", linewidth=linewidth,
    #                  markersize=cur_markersize, alpha=cur_alpha,
    #                  label=f"{sys_label} Mono SLO500",
    #                  color=color_mono)

# Load CSVs
ray_df = pd.read_csv(f"ray_cluster{cluster_size}_summary.csv")
vortex_df = pd.read_csv(f"vortex_cluster{cluster_size}_summary.csv")

# Plot Ray
plot_slo_lines(
    ray_df,
    sys_label="Ray",
    color_micro=frame_colors['Ray Microservice'],
    color_mono=frame_colors['Ray Monolithic']
)

# Plot Vortex
plot_slo_lines(
    vortex_df,
    sys_label="Typhoon",
    color_micro=frame_colors['Vortex Microservice'],
    color_mono=frame_colors['Vortex Monolithic']
)

# Titles and axes
# plt.title(f"SLO Miss Rate vs Throughput PreFLMR", fontsize=26, pad=10)
plt.xlabel('Throughput (queries/sec)', fontsize=27)
plt.ylabel('SLO Miss Rate (%)', fontsize=27)
 
# X/Y limits
if cluster_size == 7:
    plt.xlim([20, 230])
elif cluster_size == 4:
    plt.xlim([20, 120])

plt.ylim([0, 105])  # percent scale, allow a bit over 100 for visibility

plt.tick_params(axis='both', labelsize=24)
# plt.legend(fontsize=23, loc='upper left', ncol=1)
handles, labels = plt.gca().get_legend_handles_labels()
sorted_pairs = sorted(zip(labels, handles), key=lambda x: (x[0].split()[1], x[0]))
labels, handles = zip(*sorted_pairs)
plt.legend(handles, labels, fontsize=23, loc='upper left', ncol=1)

# Horizontal grid only
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig(f'{plot_name}_miss.pdf')
plt.show()

