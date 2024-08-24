import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FuncFormatter
import warnings
from process_data import *

warnings.filterwarnings("ignore")



def dot_plot_latencies(duration_df, plot_column_name, title, xaxis, yaxis, save_file_name):
     duration_df = duration_df.reset_index(drop=True)
     plt.figure(figsize=(10, 5))
     plt.plot(duration_df[plot_column_name], 'o')
     plt.title(title)
     plt.xlabel(xaxis)
     plt.ylabel(yaxis)
     plt.xticks(rotation=45)
     plt.grid()
     plt.ylim(0, duration_df[plot_column_name].max() * 1.5)
     
     plt.savefig(save_file_name)
     plt.show()




if __name__ == "__main__":
     arguments = sys.argv
     if len(sys.argv) < 3:
          print("Usage: python3 dot_plot_data.py <data_dir> <save_dir> ")
          exit()
     local_dir = sys.argv[1]
     save_dir = sys.argv[2]
     print("print_type (e2e | udl1 | udl2 | udl3 | udl1-2 | udl2-3 | udl1-2-same | udl1-2-diff | udl2-3-same | udl2-3-diff):")
     print_type = input()
     if print_type not in ["e2e", "udl1", "udl2", "udl3", "udl1-2", "udl2-3", "udl1-2-same", "udl1-2-diff", "udl2-3-same", "udl2-3-diff"]:
          print("Invalid print_type")
          exit()
     
     name =  "dotplot_" + print_type + local_dir.split("/")[-1] + ".pdf"
     save_file_name = os.path.join(save_dir, name)

     log_files = get_log_files(local_dir, suffix)
     log_data = get_log_files_dataframe(log_files)
     df = clean_log_dataframe(log_data, drop_warmup=2)
     
     if print_type == "e2e":
          duration_df = process_end_to_end_latency_dataframe(df)
          dot_plot_latencies(duration_df, 'e2e_latency', 'End-to-End Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
     elif print_type == "udl1":
          duration_df_dict = process_udl1_dataframe(df)
          dot_plot_latencies(duration_df_dict['udl1_time'], 'udl1_time', 'UDL1 Centroids Search Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
     elif print_type == "udl2":
          duration_df_dict = process_udl2_dataframe(df)
          dot_plot_latencies(duration_df_dict['udl2_time'], 'udl2_time', 'UDL2 Cluster Search Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
     elif print_type == "udl3":
          duration_df_dict = process_udl3_dataframe(df)
          dot_plot_latencies(duration_df_dict['udl3_time'], 'udl3_time', 'UDL3 Centroids Search Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
     elif print_type == "udl1-2":
          duration_df_dict = process_btw_udls(df)
          dot_plot_latencies(duration_df_dict['udl1_udl2_time'], 'udl1_udl2_time', 'UDL1-UDL2 Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
     elif print_type == "udl2-3":
          duration_df_dict = process_btw_udls(df)
          dot_plot_latencies(duration_df_dict['udl2_udl3_time'], 'udl2_udl3_time', 'UDL2-UDL3 Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
     elif print_type == "udl1-2-same":
          duration_df_dict = process_btw_udls_nodes(df)
          dot_plot_latencies(duration_df_dict['udl1_udl2_same_node_time'], 'udl1_udl2_same_node_time', 'UDL1-UDL2 SameNode Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
     elif print_type == "udl1-2-diff":
          duration_df_dict = process_btw_udls_nodes(df)
          dot_plot_latencies(duration_df_dict['udl1_udl2_diff_nodes_time'], 'udl1_udl2_diff_nodes_time', 'UDL1-UDL2 DiffNode Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
     elif print_type == "udl2-3-same":
          duration_df_dict = process_btw_udls_nodes(df)
          dot_plot_latencies(duration_df_dict['udl2_udl3_same_node_time'], 'udl2_udl3_same_node_time', 'UDL2-UDL3 SameNode Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
     elif print_type == "udl2-3-diff":
          duration_df_dict = process_btw_udls_nodes(df)
          dot_plot_latencies(duration_df_dict['udl2_udl3_diff_nodes_time'], 'udl2_udl3_diff_nodes_time', 'UDL2-UDL3 DiffNode Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)


