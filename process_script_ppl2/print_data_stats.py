import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from process_data import *

warnings.filterwarnings("ignore")

# arguments = sys.argv
# if len(sys.argv) < 2:
#      print("Usage: python print_data_stats.py <data_dir>")
#      exit()
# local_dir = sys.argv[1]

# print_type_list = ["e2e", "last_udl", "udlA", "udlB", "udlD", "udlE", "c_udla", "c_udlb", \
#           "udla_d", "udlb_d", "udld_e", "c_mono", "udlD_1", "udlD_2", "udlD_3", "throughput"]
# print(f"print_type {print_type_list}:")
# print_type = input().strip()

# if print_type not in print_type_list:
#      print("Invalid print_type")
#      exit()
# print("drop_warmup number:")
# drop_warmup_num = int(input())

# pd.set_option('display.max_columns', None)


def print_duration_df(duration_df,  column_name='e2e_latency'):
     col_width = 25
     # print("number of rows: ".ljust(col_width), len(duration_df))
     print(f"average (us): ".ljust(col_width), round(duration_df[column_name].mean(),2))
     print(f"median (us): ".ljust(col_width), round(duration_df[column_name].median(),2))
     print(f"max (us): ".ljust(col_width), round(duration_df[column_name].max(),2))
     print(f"min (us): ".ljust(col_width), round(duration_df[column_name].min(),2))
     print(f"standard deviation: ".ljust(col_width), round(duration_df[column_name].std(),2))
     

def print_udl_stats(duration_df_dict, type_name):
     print("-------- ", type_name, " --------")
     for key in duration_df_dict:
          duration_df = duration_df_dict[key]
          print("[", key, "]")
          if duration_df.empty:
               print(f"Empty dataframe for {key}, drop_warmup:{drop_warmup_num}")
               continue
          print_duration_df(duration_df,column_name=key)
     print("------------------------------------")
     
def print_avgs(duration_df_dict, type_name):
     print("-------- ", type_name, " --------")
     keys = list(duration_df_dict.keys())
     avg_durations = []
     for key in duration_df_dict:
          duration_df = duration_df_dict[key]
          if duration_df.empty:
               keys.remove(key)
               continue
          avg_durations.append(round(duration_df[key].mean(),2))
     key_width = max(len(key) for key in keys) + 1  # Adding extra space for padding
     print("items:".ljust(key_width) + "".join(f"{key}".ljust(key_width) for key in keys))
     print("Avg(us):".ljust(key_width) + "".join(f"{duration:.2f}".ljust(key_width) for duration in avg_durations))
     # print("-------------------------------------------")


if __name__ == "__main__":
     arguments = sys.argv
     if len(sys.argv) < 2:
          print("Usage: python3 dot_plot_data.py <data_dir>")
          exit()
     local_dir = sys.argv[1]
     
     list_of_type = ["e2e", "last_udl", "udlA", "udlB", "udlD", "udlE", "c_udla", "c_udlb", \
          "udla_d", "udlb_d", "udld_e", "c_mono", "udlD_1", "udlD_2", "udlD_3", "throughput"]
     print(f"print_type {list_of_type}")
     print_type = input()
     if print_type not in list_of_type:
          print("Invalid print_type")
          exit()
     
     
     
     name =  "dotplot_" + print_type + local_dir.split("/")[-1] + ".pdf"

     log_files = get_log_files(local_dir, suffix)
     log_data = get_log_files_dataframe(log_files)
     # print(f"log data: {log_data}")
     df = clean_log_dataframe(log_data, drop_warmup=50)
     
     if print_type == "e2e":
          
          duration_df = process_e2e_dataframe(df)
          print_duration_df(duration_df, 'e2e_time')
          
          
     elif print_type == "c_mono":
          duration_df_dict = process_c_mono_dataframe(df)
          print_udl_stats(duration_df_dict, "c_mono")
     
     elif print_type == "last_udl":
          duration_df_dict = process_last_udl_dataframe(df)
          print_udl_stats(duration_df_dict, "last_udl")
     
     for i in range(len(list_of_type)):
          if print_type == list_of_type[i] and i >= 2 and i <=14:
               duration_df_dict = process_bw_udls_dataframe(df)
               print_duration_df(duration_df_dict[print_type], column_name=print_type)
     
          
     if print_type == list_of_type[15]:
          throughput = compute_throughput(df)
          print(f"Throughput: {throughput} Qps")