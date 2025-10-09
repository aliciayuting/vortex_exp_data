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
import matplotlib.ticker as ticker


cluster_size = 4
plot_name = f"ppl2_vr_cluster{cluster_size}_slo"

plt.figure(figsize=(10.5, 5))
cur_markersize = 10
cur_alpha = 1.0
linewidth = 2.5

legend_items = {}  # keys like ("Ray", 600) -> handle


def plot_slo_lines(df: pd.DataFrame,
                   sys_label: str,
                   color_micro: str,
                   color_mono: str):
    """
    Plot SLO600 and SLO1000 for Micro and Mono if present.
    Expects columns:
      - ThroughputMicro, SLO600Micro, SLO1000Micro
      - ThroughputMono,  SLO600Mono,  SLO1000Mono (optional)
    """

    # --- Microservice ---
    if set(["ThroughputMicro", "SLO600Micro", "SLO1000Micro"]).issubset(df.columns):
        msk = df[["ThroughputMicro", "SLO600Micro", "SLO1000Micro"]].notna().all(axis=1)
        if msk.any():
            # SLO600
            h1, = plt.plot(df.loc[msk, "ThroughputMicro"],
                     df.loc[msk, "SLO600Micro"],
                     marker="o", linestyle="-", linewidth=linewidth,
                     markersize=cur_markersize, alpha=cur_alpha,
                     label=f"{sys_label} (600 ms SLO)",
                     color=color_micro)
            legend_items[(sys_label, 600)] = h1  
            # SLO1000 (dash-dot)
            h2, = plt.plot(df.loc[msk, "ThroughputMicro"],
                     df.loc[msk, "SLO1000Micro"],
                     marker="^", linestyle="--", linewidth=linewidth,
                     markersize=cur_markersize, alpha=cur_alpha,
                     label=f"{sys_label} (1000 ms SLO)",
                     color=color_micro)
            legend_items[(sys_label, 1000)] = h2

    # # --- Monolithic (optional) ---
    # want = {"ThroughputMono", "SLO600Mono", "SLO1000Mono"}
    # have = want.intersection(df.columns)
    # if len(have) == len(want):
    #     msk = df[["ThroughputMono", "SLO600Mono", "SLO1000Mono"]].notna().all(axis=1)
    #     if msk.any():
    #         # SLO600
    #         plt.plot(df.loc[msk, "ThroughputMono"],
    #                  df.loc[msk, "SLO600Mono"],
    #                  marker="s", linestyle="-.", linewidth=linewidth,
    #                  markersize=cur_markersize, alpha=cur_alpha,
    #                  label=f"{sys_label} Mono SLO600",
    #                  color=color_mono)
    #         # SLO1000
    #         plt.plot(df.loc[msk, "ThroughputMono"],
    #                  df.loc[msk, "SLO1000Mono"],
    #                  marker="v", linestyle=":", linewidth=linewidth,
    #                  markersize=cur_markersize, alpha=cur_alpha,
    #                  label=f"{sys_label} Mono SLO1000",
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
 
if cluster_size == 4:
    plt.xlim([5, 25])
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))

elif cluster_size == 7:
    plt.xlim([10, 45])

plt.ylim([0, 105])  # percent scale, allow a bit over 100 for visibility

plt.tick_params(axis='both', labelsize=24)
desired_order = [("Ray", 600), ("Typhoon", 600), ("Ray", 1000), ("Typhoon", 1000)]
handles = [legend_items[k] for k in desired_order if k in legend_items]
labels  = [f"{sys} ({slo} ms SLO)" for (sys, slo) in desired_order if (sys, slo) in legend_items]
plt.legend(handles, labels, fontsize=23, loc='upper left', ncol=1)


# Horizontal grid only
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig(f'{plot_name}_miss.pdf')
plt.show()

