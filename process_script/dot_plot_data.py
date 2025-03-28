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
     print(f"mean:{np.mean(np.array(duration_df[plot_column_name]))/1000.0} ms")
     print(f"median:{np.median(np.array(duration_df[plot_column_name]))/1000.0} ms")
     print(f"95 percentile: {np.percentile(np.array(duration_df[plot_column_name]), 95)/1000.0} ms")
     plt.title(title)
     plt.xlabel(xaxis)
     plt.ylabel(yaxis)
     plt.xticks(rotation=45)
     plt.grid()
     plt.ylim(0, duration_df[plot_column_name].max() * 1.5)
     
     # plt.savefig(save_file_name)
     plt.show()

def write_e2e_csv(local_dir, duration_df, throughput):
     file_name = "tp" + str(int(throughput)) + "_e2e_latency_ns.csv"
     csv_file_name = os.path.join(local_dir, file_name)
     e2e_list = duration_df['e2e_time'].tolist()
     with open(csv_file_name, 'w') as f:
          for e2e in e2e_list:
               f.write(f"{e2e},")
     f.close()
     print(f"avg e2e latency: {np.mean(np.array(e2e_list))/1000.0} ms, throughput: {throughput} Qps")
     print(f"wrote e2e csv file to {csv_file_name}")



if __name__ == "__main__":
     arguments = sys.argv
     if len(sys.argv) < 3:
          print("Usage: python3 dot_plot_data.py <data_dir> <save_dir> ")
          exit()
     local_dir = sys.argv[1]
     save_dir = sys.argv[2]
     
     list_of_type = ["e2e", "last_udl", "udlA", "udlB", "udlD", "udlE", "c_udla", "c_udlb", \
          "udla_d", "udlb_d", "udld_e", "c_mono", "udlD_1", "udlD_2", "udlD_3", "throughput",\
          "udlB_exec_batch", "udlB_emit_batch","udlD_emit_batch", "udlE_exec_batch", "udlD_exec_batch",\
          "UDLA_TP", "UDLB_TP", "UDLD_TP", "UDLE_TP", "C_A_TP", "C_B_TP", "A_D_TP", "B_D_TP", "D_E_TP", "mono_exec_batch"]
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
     df = clean_log_dataframe(log_data, start_id=1050, end_id=4999)
     throughput = compute_throughput(df)
     print(f"throughput: {throughput} Qps")
     
     if print_type == "e2e":
          duration_df = process_e2e_dataframe(df)
          print(duration_df)
          write_e2e_csv(local_dir, duration_df['e2e_time'], throughput)
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
          
     elif print_type == list_of_type[16]:
          print(f"got print type of : {print_type}")
          batch_size_df_dict = get_batch_size(df)
          print(batch_size_df_dict['udlB_exec_batch'])
          dot_plot_latencies(batch_size_df_dict['udlB_exec_batch'], 'udlB_exec_batch', 'udlB_exec_batch', \
                              'Query ID', 'Batch Size', save_file_name)
     
     elif print_type == list_of_type[17]:
          print(f"got print type of : {print_type}")
          batch_size_df_dict = get_batch_size(df)
          dot_plot_latencies(batch_size_df_dict['udlB_emit_batch'], 'udlB_emit_batch', 'udlB_emit_batch', \
                              'Query ID', 'Batch Size', save_file_name)
          
     elif print_type == list_of_type[18]:
          print(f"got print type of : {print_type}")
          batch_size_df_dict = get_batch_size(df)
          dot_plot_latencies(batch_size_df_dict['udlD_emit_batch'], 'udlD_emit_batch', 'udlD_emit_batch', \
                              'Query ID', 'Batch Size', save_file_name)
          
     elif print_type == list_of_type[19]:
          print(f"got print type of : {print_type}")
          batch_size_df_dict = get_batch_size(df)
          dot_plot_latencies(batch_size_df_dict['udlE_exec_batch'], 'udlE_exec_batch', 'udlE_exec_batch', \
                              'Query ID', 'Batch Size', save_file_name)
          
     elif print_type == list_of_type[20]:
          print(f"got print type of : {print_type}")
          batch_size_df_dict = get_batch_size(df)
          dot_plot_latencies(batch_size_df_dict['udlD_exec_batch'], 'udlD_exec_batch', 'udlD_exec_batch', \
                              'Query ID', 'Batch Size', save_file_name)
          
     elif print_type == list_of_type[21]:
          throughput = compute_udl_throughput(df,start_tag=10000, end_tag=10100)
          print(f"UDLA Throughput: {throughput} Qps")
          
     elif print_type == list_of_type[22]:
          throughput = compute_udl_throughput(df,start_tag=20000, end_tag=20031)
          print(f"UDLB Throughput: {throughput} Qps")
          
          
     elif print_type == list_of_type[23]:
          throughput = compute_udl_throughput(df,start_tag=30000, end_tag=30100)
          print(f"UDLD Throughput: {throughput} Qps")
          
          
     elif print_type == list_of_type[24]:
          throughput = compute_udl_throughput(df,start_tag=40000, end_tag=40031)
          print(f"UDLE Throughput: {throughput} Qps")
          
     elif print_type == list_of_type[25]:
          throughput = compute_udl_throughput(df,start_tag=1000, end_tag=10000)
          print(f"C_A Throughput: {throughput} Qps")
          
     elif print_type == list_of_type[26]:
          throughput = compute_udl_throughput(df,start_tag=1000, end_tag=20000)
          print(f"C_B Throughput: {throughput} Qps")
          
     elif print_type == list_of_type[27]:
          throughput = compute_udl_throughput(df,start_tag=10100, end_tag=30000)
          print(f"A_D Throughput: {throughput} Qps")
          
     elif print_type == list_of_type[28]:
          throughput = compute_udl_throughput(df,start_tag=20031, end_tag=30010)
          print(f"B_D Throughput: {throughput} Qps")
          
     elif print_type == list_of_type[29]:
          throughput = compute_udl_throughput(df,start_tag=30100, end_tag=40000)
          print(f"D_E Throughput: {throughput} Qps")
          
          
     elif print_type == list_of_type[30]:
          print(f"got print type of : {print_type}")
          batch_size_df_dict = get_batch_size(df)
          print(batch_size_df_dict['mono_exec_batch'])
          dot_plot_latencies(batch_size_df_dict['mono_exec_batch'], 'mono_exec_batch', 'mono_exec_batch', \
                              'Query ID', 'Batch Size', save_file_name)
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

