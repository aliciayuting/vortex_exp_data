import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter

from process_data import (
    get_log_files,
    get_log_files_dataframe,
    clean_log_dataframe,
    compute_throughput,
    process_e2e_dataframe_with_starttime,
)

def write_e2e_csv(local_dir, duration_df, throughput):
    file_name = "tp" + str(int(throughput)) + "_e2e_latency_ns.csv"
    csv_file_name = os.path.join(local_dir, file_name)
    e2e_list = duration_df['e2e_time'].tolist()
    with open(csv_file_name, 'w') as f:
        for e2e in e2e_list:
            f.write(f"{e2e},")
    print(f"avg e2e latency: {np.mean(np.array(e2e_list))/1000.0} ms, throughput: {throughput} Qps")
    print(f"wrote e2e csv file to {csv_file_name}")


def seconds_to_mmss(x, _):
    minutes = int(x // 60)
    seconds = int(x % 60)
    return f"{minutes:02}:{seconds:02}"

def dot_plot_latencies(duration_df, plot_column_name, title, xaxis, yaxis, save_path):
    x_vals = (duration_df['timestamp'] - duration_df['timestamp'].min()) / 1e3  # µs → ms
    y_vals = duration_df[plot_column_name] / 1e3  # ns → ms for latency
    print(f"count the number of ys exceeding 1000ms:{len(y_vals[y_vals > 500])}, {len(y_vals[y_vals > 500])/9899}")
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(x_vals, y_vals, 'o', markersize=3.8)

    ax.set_title(title, fontsize=28)
    ax.set_xlabel(xaxis, fontsize=24)
    ax.set_ylabel(yaxis, fontsize=24)
    ax.tick_params(axis='x', labelsize=18)
    ax.tick_params(axis='y', labelsize=22)
    ax.set_ylim(0, 8000)
    ax.grid(True, linestyle='--', alpha=0.6)

    # # Format x-axis as MM:SS with ticks every 10 seconds
    # def ms_to_mmss(x, _):
    #     total_seconds = int(x // 1000)
    #     minutes = total_seconds // 60
    #     seconds = total_seconds % 60
    #     return f"{minutes:02}:{seconds:02}"

    # ax.xaxis.set_major_locator(MultipleLocator(10000))  # every 10s
    # ax.xaxis.set_major_formatter(FuncFormatter(ms_to_mmss))
    # plt.xticks(rotation=45)

    plt.tight_layout()
    # plt.savefig(save_path)
    # plt.show()


def process_input_folder(folder):
    log_files = get_log_files(folder, suffix)
    log_data = get_log_files_dataframe(log_files)
    df = clean_log_dataframe(log_data, start_id=4000, end_id=9999)
    throughput = compute_throughput(df)
    duration_df = process_e2e_dataframe_with_starttime(df)['e2e_time']
    return duration_df, throughput


if __name__ == "__main__":
    input_dir1 = "4-3cloudlab_micro_scale/cluster4t7_warmup/sendrate_70_130/"
    input_dir2 = "4-3cloudlab_micro_scale/no_warmup_cluster4t7/sendrate_70_130/"
    save_dir = './'

    suffix = ".dat"

    # Process and plot first input directory
    df1, tp1 = process_input_folder(input_dir1)
    save_file1 = os.path.join(save_dir, "temp_timestamp_dotplot_e2e_warmup.pdf")
    dot_plot_latencies(df1, 'e2e_time', 'Warmup End-to-End Latency', 'Elapsed Time (MM:SS)', 'Latency (ms)', save_file1)

#     Uncomment this block if you want to also plot the no-warmup version
    df2, tp2 = process_input_folder(input_dir2)
    save_file2 = os.path.join(save_dir, "temp_timestamp_dotplot_e2e_no_warmup.pdf")
    dot_plot_latencies(df2, 'e2e_time', 'No Warmup End-to-End Latency', 'Elapsed Time (MM:SS)', 'Latency (ms)', save_file2)