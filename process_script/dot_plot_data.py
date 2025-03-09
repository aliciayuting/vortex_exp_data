import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FuncFormatter
import warnings
from process_data import *
import numpy as np
warnings.filterwarnings("ignore")



def dot_plot_latencies(duration_df, plot_column_name, title, xaxis, yaxis, save_file_name):
     duration_df = duration_df.reset_index(drop=True)
     plt.figure(figsize=(10, 5))
     # plt.plot(duration_df[plot_column_name], 'o')
     plt.plot(duration_df['node_id'], duration_df[plot_column_name], 'o')
     # print(duration_df['node_id'])
     print(np.median(np.array(duration_df[plot_column_name])))

     plt.title(title)
     plt.xlabel(xaxis)
     plt.ylabel(yaxis)
     plt.xticks(rotation=45)
     plt.grid()
     plt.ylim(0, duration_df[plot_column_name].max() * 1.5)
     
     # plt.savefig(save_file_name)
     # plt.show()




if __name__ == "__main__":
     arguments = sys.argv
     if len(sys.argv) < 3:
          print("Usage: python3 dot_plot_data.py <data_dir> <save_dir> ")
          exit()
     local_dir = sys.argv[1]
     save_dir = sys.argv[2]
     
     list_of_type = ["e2e", "last_udl", "udlA", "udlB", "udlD", "udlE", "c_udla", "c_udlb", \
          "udla_d", "udlb_d", "udld_e", "c_mono", "udlD_1", "udlD_2", "udlD_3", "throughput"]
     print(f"print_type {list_of_type}")
     print_type = input()
     if print_type not in list_of_type:
          print("Invalid print_type")
          exit()
     
     
     
     name =  "dotplot_" + print_type + local_dir.split("/")[-1] + ".pdf"
     save_file_name = os.path.join(save_dir, name)

     log_files = get_log_files(local_dir, suffix)
     log_data = get_log_files_dataframe(log_files)
     # print(f"log data: {log_data}")
     df = clean_log_dataframe(log_data, drop_warmup=50)
     
     if print_type == "e2e":
          
          duration_df = process_e2e_dataframe(df)
          print(duration_df)
          
          dot_plot_latencies(duration_df['e2e_time'], 'e2e_time', 'End-to-End Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
          
     elif print_type == "c_mono":
          duration_df_dict = process_c_mono_dataframe(df)
          dot_plot_latencies(duration_df_dict['c_mono'], 'c_mono', 'c_mono Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
     
     elif print_type == "last_udl":
          duration_df_dict = process_last_udl_dataframe(df)
          dot_plot_latencies(duration_df_dict['last_udl_time'], 'last_udl_time', 'last_udl_time Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
     elif print_type == "udlA":
          duration_df_dict = process_udls_dataframe(df)
          dot_plot_latencies(duration_df_dict['udlA'], 'udlA', 'udlA Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
          
     elif print_type == "udlB":
          duration_df_dict = process_udls_dataframe(df)
          dot_plot_latencies(duration_df_dict['udlB'], 'udlB', 'udlB_time Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
          
     elif print_type == "udlD":
          duration_df_dict = process_udls_dataframe(df)
          dot_plot_latencies(duration_df_dict['udlD'], 'udlD', 'udlD_time Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
          
     elif print_type == "udlE":
          duration_df_dict = process_udls_dataframe(df)
          dot_plot_latencies(duration_df_dict['udlE'], 'udlE', 'udlE_time Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
          
     elif print_type == list_of_type[6]:
          duration_df_dict = process_bw_udls_dataframe(df)
          dot_plot_latencies(duration_df_dict['c_udla'], 'c_udla', 'c_udla Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
          
     elif print_type == list_of_type[7]:
          duration_df_dict = process_bw_udls_dataframe(df)
          dot_plot_latencies(duration_df_dict['c_udlb'], 'c_udlb', 'c_udlb Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
          
     elif print_type == list_of_type[8]:
          duration_df_dict = process_bw_udls_dataframe(df)
          dot_plot_latencies(duration_df_dict['udla_d'], 'udla_d', 'udla_d Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
     
     elif print_type == list_of_type[9]:
          duration_df_dict = process_bw_udls_dataframe(df)
          dot_plot_latencies(duration_df_dict[print_type], print_type, f'{print_type} Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
          
     elif print_type == list_of_type[10]:
          duration_df_dict = process_bw_udls_dataframe(df)
          dot_plot_latencies(duration_df_dict[print_type], print_type, f'{print_type} Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
          
     elif print_type == list_of_type[12]:
          print(f"got print type of : {print_type}")
          duration_df_dict = process_udlD_dataframe(df)
          dot_plot_latencies(duration_df_dict[print_type], print_type, f'{print_type} Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
     
     elif print_type == list_of_type[13]:
          print(f"got print type of : {print_type}")
          duration_df_dict = process_udlD_dataframe(df)
          dot_plot_latencies(duration_df_dict[print_type], print_type, f'{print_type} Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
          
     elif print_type == list_of_type[14]:
          print(f"got print type of : {print_type}")
          duration_df_dict = process_udlD_dataframe(df)
          dot_plot_latencies(duration_df_dict[print_type], print_type, f'{print_type} Latency(us)', \
                              'Query ID', 'Latency (us)', save_file_name)
          
     elif print_type == list_of_type[15]:
          throughput = compute_throughput(df)
          print(f"Throughput: {throughput} Qps")
          
     # elif print_type == "udl2":
     #      duration_df_dict,_ = process_udl2_dataframe(df)
     #      dot_plot_latencies(duration_df_dict['udl2_time'], 'udl2_time', 'UDL2 Cluster Search Latency(us)', \
     #                          'Query ID', 'Latency (us)', save_file_name)
     # elif print_type == "udl3":
     #      duration_df_dict = process_udl3_dataframe(df)
     #      dot_plot_latencies(duration_df_dict['udl3_time'], 'udl3_time', 'UDL3 Centroids Search Latency(us)', \
     #                          'Query ID', 'Latency (us)', save_file_name)
     # elif print_type == "udl1-2":
     #      duration_df_dict = process_btw_udls(df)
     #      dot_plot_latencies(duration_df_dict['udl1_udl2_time'], 'udl1_udl2_time', 'UDL1-UDL2 Latency(us)', \
     #                          'Query ID', 'Latency (us)', save_file_name)
     # elif print_type == "udl2-3":
     #      duration_df_dict = process_btw_udls(df)
     #      dot_plot_latencies(duration_df_dict['udl2_udl3_time'], 'udl2_udl3_time', 'UDL2-UDL3 Latency(us)', \
     #                          'Query ID', 'Latency (us)', save_file_name)
     # elif print_type == "udl1-2-same":
     #      duration_df_dict = process_btw_udls_nodes(df)
     #      dot_plot_latencies(duration_df_dict['udl1_udl2_same_node_time'], 'udl1_udl2_same_node_time', 'UDL1-UDL2 SameNode Latency(us)', \
     #                          'Query ID', 'Latency (us)', save_file_name)
     # elif print_type == "udl1-2-diff":
     #      duration_df_dict = process_btw_udls_nodes(df)
     #      dot_plot_latencies(duration_df_dict['udl1_udl2_diff_nodes_time'], 'udl1_udl2_diff_nodes_time', 'UDL1-UDL2 DiffNode Latency(us)', \
     #                          'Query ID', 'Latency (us)', save_file_name)
     # elif print_type == "udl2-3-same":
     #      duration_df_dict = process_btw_udls_nodes(df)
     #      dot_plot_latencies(duration_df_dict['udl2_udl3_same_node_time'], 'udl2_udl3_same_node_time', 'UDL2-UDL3 SameNode Latency(us)', \
     #                          'Query ID', 'Latency (us)', save_file_name)
     # elif print_type == "udl2-3-diff":
     #      duration_df_dict = process_btw_udls_nodes(df)
     #      dot_plot_latencies(duration_df_dict['udl2_udl3_diff_nodes_time'], 'udl2_udl3_diff_nodes_time', 'UDL2-UDL3 DiffNode Latency(us)', \
     #                          'Query ID', 'Latency (us)', save_file_name)

