import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np

import matplotlib as mpl
mpl.rcParams.update({
    "text.usetex": False,
    "font.family": "serif",
    "font.serif": ["Computer Modern", "Latin Modern Roman", "CMU Serif", "DejaVu Serif"],
    "pdf.fonttype": 42,
    "ps.fonttype": 42
})

def plot_best_stacked_throughput(csv_path, output_path="best_stacked_throughput.pdf"):
    # === Load data ===
    df = pd.read_csv(csv_path)

    # === Step 1: Find best-performing batch size per config ===
    total_tp_by_config_batch = df.groupby(["config", "batch_size"])["throughput"].sum().reset_index()
    best_batch_per_config = total_tp_by_config_batch.loc[
        total_tp_by_config_batch.groupby("config")["throughput"].idxmax()
    ][["config", "batch_size"]]

    # === Step 2: Filter original df to keep only best batch per config ===
    df_best = df.merge(best_batch_per_config, on=["config", "batch_size"])

    # === Step 3: Create pivot table for stacked bar plot ===
    pivot = df_best.pivot_table(
        index="config",
        columns="component",
        values="throughput",
        aggfunc="sum",
        fill_value=0
    )

    # Sort component columns numerically
    pivot = pivot[sorted(pivot.columns, key=lambda x: int(x.split('_')[1]))]

    # === Step 4: Rename and reorder config labels for clean x-axis ===
    label_map = {
        "NOMIG": "NoMIG",
        "processes2": "2 processes",
        "MIG2": "2xMIG12g",
        "processes4": "4 processes",
        "MIG4": "4xMIG6g"
    }
    desired_order = ["NOMIG", "processes2",  "processes4","MIG2", "MIG4"]
    pivot = pivot.reindex(desired_order).dropna(how="all")
    pivot.index = [label_map.get(cfg, cfg) for cfg in pivot.index]

    # === Step 5: Plot using serious yellow and black outlines ===
    serious_yellow = "#f6e199"


    ax = pivot.plot(
        kind="bar",
        stacked=True,
        figsize=(12, 6),
        color=[serious_yellow] * len(pivot.columns),
        edgecolor="black",
        linewidth=4  # <-- Thicker outlines
    )
    y_max = ax.get_ylim()[1]
    ax.set_yticks(np.arange(0, y_max + 1, 50))
    plt.ylabel("Throughput (queries/sec)", fontsize=28)
    # plt.xlabel("Deployment Configuration", fontsize=24)
    # plt.title("Throughput on one GPU", fontsize=25)
    plt.xticks(rotation=15, ha="center", fontsize=27)
    plt.yticks(fontsize=27)
    # Remove legend if it was generated
    if ax.get_legend() is not None:
        ax.get_legend().remove()
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot best-case stacked throughput per deployment")
    parser.add_argument("csv", type=str, help="CSV file with throughput summary")
    parser.add_argument("-o", "--output", type=str, default="stepE_stacked_throughput.pdf",
                        help="Output PDF filename")
    args = parser.parse_args()

    plot_best_stacked_throughput(args.csv, args.output)