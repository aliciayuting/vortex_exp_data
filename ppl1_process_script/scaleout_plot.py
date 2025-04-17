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


def seconds_to_mmss(x, _):
    minutes = int(x // 60)
    seconds = int(x % 60)
    return f"{minutes:02}:{seconds:02}"


def dot_plot_latencies(duration_df, plot_column_name, title, xaxis, yaxis,highlight_start, highlight_end , save_file_name):
     duration_df = duration_df.reset_index(drop=True)
    #  plt.figure(figsize=(23, 9))
     fig, ax = plt.subplots(figsize=(21, 8))
     plt.subplots_adjust(left=0.1, right=0.98, top=0.92, bottom=0.15)

     # plt.plot(duration_df[plot_column_name], 'o')
     duration_df[plot_column_name] = duration_df[plot_column_name] / 10**3
     
     plt.plot(duration_df['node_id'], duration_df[plot_column_name], 'o', markersize=3.8)
     # print(duration_df['node_id'])
     print(f"mean:{np.mean(np.array(duration_df[plot_column_name]))/1000.0} ms")
     print(f"median:{np.median(np.array(duration_df[plot_column_name]))/1000.0} ms")
     print(f"95 percentile: {np.percentile(np.array(duration_df[plot_column_name]), 95)/1000.0} ms")
     plt.tight_layout(pad=2.0, rect=[0.45, 3.5, 0.45, 0.95])     # plt.subplots_adjust(top=0.95)
     plt.title(title, fontsize=36)
     plt.xlabel(xaxis, fontsize=33, labelpad=0.05)
     plt.ylabel(yaxis, fontsize=33)
     plt.xticks(fontsize=33)
     plt.yticks(fontsize=33)
     plt.yticks(fontsize=33)
     plt.gca().yaxis.set_major_locator(MultipleLocator(2000))
     
     y_pos = 7100
     
     plt.annotate(" ", 
                  xy=(0, y_pos), 
                  xytext=(2000, y_pos), 
                  arrowprops=dict(arrowstyle="<->", 
                                  color="red", 
                                  mutation_scale=33,
                                  lw=5),
     )
     plt.text(
          (0 + 2000) / 2, y_pos + 160, 
          "SR: 70 QPS", 
          horizontalalignment='center', 
          color='red',
          fontsize=33,
     )
     
     plt.annotate(" ", 
                  xy=(2000, y_pos), 
                  xytext=(8000, y_pos), 
                  arrowprops=dict(arrowstyle="<->", 
                                  color="red", 
                                  mutation_scale=33,
                                  lw=5),
     )
     plt.text(
          (2000 + 8000) / 2, y_pos + 160, 
          "SR: 180 QPS", 
          horizontalalignment='center', 
          color='red',
          fontsize=33,
     )
     
     
     y_pos2 = 6700
     plt.annotate(" ", 
                  xy=(0, y_pos2), 
                  xytext=(4000, y_pos2), 
                  arrowprops=dict(arrowstyle="<->", 
                                  color="green", 
                                  mutation_scale=33,
                                  lw=5),
     )
     plt.text(
          (0 + 4000) / 2, y_pos2 - 500, 
          "4 Nodes", 
          horizontalalignment='center', 
          color='green',
          fontsize=33,
     )
     plt.annotate(" ", 
                  xy=(4000, y_pos2), 
                  xytext=(8000, y_pos2), 
                  arrowprops=dict(arrowstyle="<->", 
                                  color="green", 
                                  mutation_scale=33,
                                  lw=5),
     )
     plt.text(
          (4000 + 8000) / 2, y_pos2 - 500, 
          "7 Nodes", 
          horizontalalignment='center', 
          color='green',
          fontsize=33,
     )
     
     plt.grid()
     plt.ylim(0, 8000)
     
     # Highlight a region (e.g., warmup period)
     ax.axvspan(highlight_start,highlight_end, color='gray', alpha=0.2)
    #  ax.text(5, 1008.5, "Warmup", ha='center', fontsize=16)
     ax.axhline(y=1000, color='red', linestyle='--', linewidth=2)
     ax.text(duration_df['node_id'].iloc[-1], 1000 + 120, '1000ms SLO', color='red', fontsize=28,
        verticalalignment='bottom', horizontalalignment='right')
     
     plt.savefig(save_file_name)
     plt.show()



def process_input_folder(folder):
    log_files = get_log_files(folder, suffix)
    log_data = get_log_files_dataframe(log_files)
    df = clean_log_dataframe(log_data, start_id=100, end_id=7999)
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
    save_file1 = os.path.join(save_dir, "dotplot_e2e_warmup_grayed_1000slo.pdf")
    dot_plot_latencies(df1, 'e2e_time', 'End-to-End Latency by Query', 'Query ID', 'Latency (ms)',4000,4250, save_file1)

#     Uncomment this block if you want to also plot the no-warmup version
    df2, tp2 = process_input_folder(input_dir2)
    save_file2 = os.path.join(save_dir, "dotplot_e2e_no_warmup_grayed_1000slo.pdf")
    dot_plot_latencies(df2, 'e2e_time', 'End-to-End Latency by Query', 'Query ID', 'Latency (ms)', 4000,5850, save_file2)