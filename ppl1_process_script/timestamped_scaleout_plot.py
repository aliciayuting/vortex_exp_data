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

def dot_plot_latencies(duration_df, plot_column_name, title, xaxis, yaxis,
                       highlight_start, highlight_end , save_file_name,
                       x1_start=None, x2_start=None, x_end=None):
    x_vals = (duration_df['timestamp'] - duration_df['timestamp'].min()) / 1e6  # µs → s
    y_vals = duration_df[plot_column_name] / 1e3  # ns → ms for latency
    # print(f"count the number of ys exceeding 1000ms:{len(y_vals[y_vals > 1000])}")
    fig, ax = plt.subplots(figsize=(21, 8))
    plt.subplots_adjust(left=0.1, right=0.98, top=0.92, bottom=0.15)

    ax.plot(x_vals, y_vals, 'o', markersize=3.8)

    print(f"mean:{np.mean(np.array(duration_df[plot_column_name]))/1000.0} ms")
    print(f"median:{np.median(np.array(duration_df[plot_column_name]))/1000.0} ms")
    print(f"95 percentile: {np.percentile(np.array(duration_df[plot_column_name]), 95)/1000.0} ms")
    print(f"number of points exceeds 500ms: {len(y_vals[y_vals > 500])}")
    print(f"number of points exceeds 1000ms: {len(y_vals[y_vals > 1000])}")
    print(f"max x value: {max(x_vals)}")
    plt.tight_layout(pad=2.0, rect=[0.45, 3.5, 0.45, 0.95])     # plt.subplots_adjust(top=0.95)
    plt.title(title, fontsize=38)
    plt.xlabel(xaxis, fontsize=37, labelpad=0.05)
    plt.ylabel(yaxis, fontsize=37)
    plt.xticks(fontsize=36)
    plt.yticks(fontsize=36)
    plt.gca().yaxis.set_major_locator(MultipleLocator(2000))
    y_pos = 7100
     
    plt.annotate(" ", 
                xy=(0, y_pos), 
                xytext=(x1_start, y_pos), 
                arrowprops=dict(arrowstyle="<->", 
                                color="red", 
                                mutation_scale=33,
                                lw=5),
    )
    plt.text(
        (0 + x1_start) / 2, y_pos + 160, 
        "SR: 70 QPS", 
        horizontalalignment='center', 
        color='red',
        fontsize=38,
    )
    
    plt.annotate(" ", 
                xy=(x1_start, y_pos), 
                xytext=(x_end, y_pos), 
                arrowprops=dict(arrowstyle="<->", 
                                color="red", 
                                mutation_scale=33,
                                lw=5),
    )
    plt.text(
        (x1_start + x_end) / 2, y_pos + 160, 
        "SR: 130 QPS", 
        horizontalalignment='center', 
        color='red',
        fontsize=38,
    )
    
    
    y_pos2 = 6700
    plt.annotate(" ", 
                xy=(0, y_pos2), 
                xytext=(x2_start, y_pos2), 
                arrowprops=dict(arrowstyle="<->", 
                                color="green", 
                                mutation_scale=36,
                                lw=5),
    )
    plt.text(
        (0 + x2_start) / 2, y_pos2 - 650, 
        "4 Nodes", 
        horizontalalignment='center', 
        color='green',
        fontsize=38,
    )
    plt.annotate(" ", 
                xy=(x2_start, y_pos2), 
                xytext=(x_end, y_pos2), 
                arrowprops=dict(arrowstyle="<->", 
                                color="green", 
                                mutation_scale=36,
                                lw=5),
    )
    plt.text(
        (x2_start + x_end) / 2, y_pos2 - 650, 
        "7 Nodes", 
        horizontalalignment='center', 
        color='green',
        fontsize=38,
    )
    
    plt.grid()
    plt.ylim(0, 8000)
    plt.xlim(0, x_end)

    # # Format x-axis as MM:SS with ticks every 10 seconds
    # def ms_to_mmss(x, _):
    #     total_seconds = int(x // 1000)
    #     minutes = total_seconds // 60
    #     seconds = total_seconds % 60
    #     return f"{minutes:02}:{seconds:02}"

    # ax.xaxis.set_major_locator(MultipleLocator(10000))  # every 10s
    # ax.xaxis.set_major_formatter(FuncFormatter(ms_to_mmss))
    # plt.xticks(rotation=45)
    
    # ax.axvspan(highlight_start,highlight_end, color='gray', alpha=0.2)

    plt.tight_layout()
    # plt.savefig(save_file_name)
    plt.show()


def process_input_folder(folder):
    log_files = get_log_files(folder, suffix)
    log_data = get_log_files_dataframe(log_files)
    df = clean_log_dataframe(log_data, start_id=500, end_id=5900)
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
    dot_plot_latencies(df1, 'e2e_time', 'End-to-End Latency by Query', 'Elapsed Time (s)', 
                       'Latency (ms)',4000,4250, save_file1,
                       x1_start=21.88, x2_start=38.277,x_end=80)

#     Uncomment this block if you want to also plot the no-warmup version
    df2, tp2 = process_input_folder(input_dir2)
    save_file2 = os.path.join(save_dir, "temp_timestamp_dotplot_e2e_no_warmup.pdf")
    dot_plot_latencies(df2, 'e2e_time', 'No Warmup End-to-End Latency by Query', 'Elapsed Time (s)',
                        'Latency (ms)',4000,4250, save_file1,
                        x1_start=21.82, x2_start=38.152,x_end=80)
