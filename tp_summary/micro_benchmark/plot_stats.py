import argparse
import pandas as pd
import matplotlib.pyplot as plt

# === Global option to toggle latency plotting ===
PLOT_LATENCY = False

def plot_throughput_and_latency(csv_path, output_file="latency_throughput_plot.pdf"):
    df = pd.read_csv(csv_path)
    df = df.sort_values(by=["type", "batch_size"])

    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.set_xlabel("Batch Size")
    ax1.set_ylabel("Throughput (queries/sec)")

    step_types = sorted(df["type"].unique())
    colors = plt.get_cmap("tab10").colors

    # Create secondary axis only if needed
    ax2 = ax1.twinx() if PLOT_LATENCY else None
    if ax2:
        ax2.set_ylabel("Average Latency (ms)")

    for i, step in enumerate(step_types):
        subset = df[df["type"] == step]
        
        # Plot throughput on the left
        ax1.plot(
            subset["batch_size"],
            subset["throughput"],
            marker='o',
            linestyle='-',
            label=f"{step} throughput",
            color=colors[i]
        )

        # Plot latency on the right if enabled
        if PLOT_LATENCY and ax2:
            ax2.plot(
                subset["batch_size"],
                subset["avg_latency_ms"],
                marker='x',
                linestyle='--',
                label=f"{step} latency",
                color=colors[i]
            )

    ax1.set_title("Throughput (L) and Latency (R) vs. Batch Size for Each Step")
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Combine legends from both axes
    handles, labels = ax1.get_legend_handles_labels()
    if PLOT_LATENCY and ax2:
        handles2, labels2 = ax2.get_legend_handles_labels()
        handles += handles2
        labels += labels2

    ax1.legend(handles, labels, loc="upper left")

    plt.tight_layout()
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot throughput (and optionally latency) from summary CSV")
    parser.add_argument("csv", type=str, help="Path to summary CSV")
    parser.add_argument("output_prefix", type=str, help="Prefix for output PDF file")
    args = parser.parse_args()

    output_filename = args.output_prefix + "_all_steps_latency_throughput_plot.pdf"
    plot_throughput_and_latency(args.csv, output_filename)