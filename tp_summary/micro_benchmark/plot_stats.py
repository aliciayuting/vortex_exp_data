import argparse
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

# Custom label and color maps
label_map = {
    "stepA": "TextEncoder",
    "stepB": "VisionEncoder",
    "stepCD": "CrossAttn",
    "stepE": "ColbertSearch"
}

# color_map = {
#     "stepA": "#f8766d",     # light red
#     "stepB": "#00ba38",     # green
#     "stepCD": "#619cff",    # blue
#     "stepE": "#f6c141"      # yellow
# }
color_map = {
    "stepA": "#b2182b",     # deep red
    "stepB": "#1a9850",     # forest green
    "stepCD": "#2166ac",    # rich blue
    "stepE": "#d8b365"      # muted golden yellow
}

def plot_facet_per_step(csv_path, output_prefix, y_limit=2500):
    output_file = output_prefix + "_facet_plot.pdf"
    df = pd.read_csv(csv_path)
    step_types = sorted(df["type"].unique())
    num_steps = len(step_types)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10), sharex=True)
    axes = axes.flatten()

    plt.rcParams.update({
        "font.size": 14,
        "axes.titlesize": 16,
        "axes.labelsize": 14,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "legend.fontsize": 12
    })

    for i, step in enumerate(step_types):
        ax = axes[i]
        subset = df[df["type"] == step]
        label = label_map.get(step, step)
        color = color_map.get(step, "gray")

        ax.plot(subset["batch_size"], subset["throughput"], marker='o',
                label="Throughput", color=color, linestyle='-', linewidth=2.5, markersize=6)
        ax.plot(subset["batch_size"], subset["gpu_max_mem_MB"], marker='s',
                label="Max GPU Mem", color=color, linestyle='--', linewidth=2.5, markersize=6)

        ax.set_title(label)
        ax.set_ylabel("Value")
        ax.set_ylim(0, y_limit)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(loc="upper left")

    for j in range(num_steps, 4):
        fig.delaxes(axes[j])

    axes[-2].set_xlabel("Batch Size")
    axes[-1].set_xlabel("Batch Size")

    fig.suptitle("Throughput and GPU Max Memory per Step", fontsize=18)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(output_file)
    print(f"Facet plot saved to {output_file}")
    plt.show()


def plot_throughput_and_memory_split(csv_path, output_prefix, y_limit_tp=None, y_limit_mem=None):
    output_file = output_prefix + "_ppl1_throughput_gpu_mem_batch_plot.pdf"
    df = pd.read_csv(csv_path)
    df = df.sort_values(by=["type", "batch_size"])
    step_types = sorted(df["type"].unique())

    plt.rcParams.update({
        "font.size": 25,
        "axes.titlesize": 25,
        "axes.labelsize": 25,
        "xtick.labelsize": 23,
        "ytick.labelsize": 23,
        "legend.fontsize": 25
    })

    fig, (ax_tp, ax_mem) = plt.subplots(1, 2, figsize=(17, 7), sharex=True)

    # Throughput plot (left)
    for step in step_types:
        subset = df[df["type"] == step]
        ax_tp.plot(
            subset["batch_size"], subset["throughput"],
            marker='o', linestyle='-', linewidth=3.9, markersize=10,
            color=color_map.get(step, "gray"),
            label=label_map.get(step, step)
        )
    ax_tp.set_xlabel("Batch Size", fontsize=27)
    ax_tp.set_ylabel("Throughput (queries/sec)", fontsize=27)
    ax_tp.set_title("Throughput Achieved", fontsize=28)
    ax_tp.grid(True, linestyle='--', alpha=0.7)
    if y_limit_tp:
        ax_tp.set_ylim(0, y_limit_tp)
        
    
    # GPU memory plot (right)
    for step in step_types:
        subset = df[df["type"] == step]
        ax_mem.plot(
            subset["batch_size"], subset["gpu_max_mem_MB"],
            marker='s', linestyle='--', linewidth=3.9, markersize=10,
            color=color_map.get(step, "gray"),
            label=label_map.get(step, step)
        )
    ax_mem.set_xlabel("Batch Size", fontsize=27)
    ax_mem.set_ylabel("Max GPU Memory (MB)", fontsize=27)
    ax_mem.set_title("GPU Memory Usage", fontsize=28)
    ax_mem.grid(True, linestyle='--', alpha=0.7)
    if y_limit_mem:
        ax_mem.set_ylim(0, y_limit_mem)

    ax_mem.legend(
        loc="center right",
        bbox_to_anchor=(1.0, 0.5),
        frameon=True,  # Optional: add border to make it stand out
        prop={"size": 25}
    )

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(output_file)
    print(f"Side-by-side plot saved to {output_file}")
    plt.show()

def plot_throughput_memory_util_split(csv_path, output_prefix, y_limit_tp=None, y_limit_mem=None, y_limit_util=110):
    output_file = output_prefix + "_ppl1_throughput_gpu_mem_util_batch_plot.pdf"
    df = pd.read_csv(csv_path)
    df = df.sort_values(by=["type", "batch_size"])
    step_types = sorted(df["type"].unique())

    plt.rcParams.update({
        "font.size": 25,
        "axes.titlesize": 25,
        "axes.labelsize": 25,
        "xtick.labelsize": 23,
        "ytick.labelsize": 23,
        "legend.fontsize": 22
    })

    fig, (ax_tp, ax_mem, ax_util) = plt.subplots(1, 3, figsize=(25, 7), sharex=True)

    # Throughput plot (left)
    for step in step_types:
        subset = df[df["type"] == step]
        ax_tp.plot(
            subset["batch_size"], subset["throughput"],
            marker='o', linestyle='-', linewidth=3.5, markersize=9,
            color=color_map.get(step, "gray"),
            label=label_map.get(step, step)
        )
    ax_tp.set_xlabel("Batch Size", fontsize=27)
    ax_tp.set_ylabel("Throughput (queries/sec)", fontsize=27)
    ax_tp.set_title("Throughput Achieved", fontsize=28)
    ax_tp.grid(True, linestyle='--', alpha=0.7)
    if y_limit_tp:
        ax_tp.set_ylim(0, y_limit_tp)

    # GPU memory plot (middle)
    for step in step_types:
        subset = df[df["type"] == step]
        ax_mem.plot(
            subset["batch_size"], subset["gpu_max_mem_MB"],
            marker='s', linestyle='--', linewidth=3.5, markersize=9,
            color=color_map.get(step, "gray"),
            label=label_map.get(step, step)
        )
    ax_mem.set_xlabel("Batch Size", fontsize=27)
    ax_mem.set_ylabel("Max GPU Memory (MB)", fontsize=27)
    ax_mem.set_title("GPU Memory Usage", fontsize=28)
    ax_mem.grid(True, linestyle='--', alpha=0.7)
    if y_limit_mem:
        ax_mem.set_ylim(0, y_limit_mem)

    # GPU utilization plot (right)
    for step in step_types:
        subset = df[df["type"] == step]
        ax_util.plot(
            subset["batch_size"], subset["gpu_max_util_percent"],
            marker='^', linestyle=':', linewidth=3.5, markersize=9,
            color=color_map.get(step, "gray"),
            label=label_map.get(step, step)
        )
    ax_util.set_xlabel("Batch Size", fontsize=27)
    ax_util.set_ylabel("Max GPU Utilization (%)", fontsize=27)
    ax_util.set_title("GPU Utilization", fontsize=28)
    ax_util.grid(True, linestyle='--', alpha=0.7)
    if y_limit_util:
        ax_util.set_ylim(0, y_limit_util)

    # Put the legend inside the last plot (ax_util)
    ax_util.legend(
        loc="upper right",   # or use 'center left' if you want lower
        frameon=True,
        fontsize=22,
        borderpad=0.5,
        handlelength=1.5
    )

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(output_file)
    print(f"Side-by-side (3-panel) plot saved to {output_file}")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot throughput and GPU memory vs. batch size")
    parser.add_argument("csv", type=str, help="Input CSV file with summary data")
    parser.add_argument("output_prefix", type=str, help="Prefix for the output PDF file", default="plot")
    parser.add_argument("--mode", type=str, choices=["facet", "side"], default="facet",
                        help="Plot mode: 'facet' for 2x2 per-step, 'side' for split view")
    parser.add_argument("--ylim", type=int, default=2500, help="Y-axis limit for facet plots")
    parser.add_argument("--ylim_tp", type=int, default=None, help="Y-axis limit for throughput (side mode)")
    parser.add_argument("--ylim_mem", type=int, default=None, help="Y-axis limit for memory (side mode)")
    args = parser.parse_args()


    # plot_facet_per_step(args.csv, args.output_prefix, y_limit=args.ylim)

    # plot_throughput_and_memory_split(
    #     args.csv, args.output_prefix,
    #     y_limit_tp=args.ylim_tp,
    #     y_limit_mem=args.ylim_mem
    # )
    
    plot_throughput_memory_util_split(
        args.csv, args.output_prefix,
        y_limit_tp=args.ylim_tp,
        y_limit_mem=args.ylim_mem
    )