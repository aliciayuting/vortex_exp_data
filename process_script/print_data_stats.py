import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from process_data import *

warnings.filterwarnings("ignore")

arguments = sys.argv
if len(sys.argv) < 2:
     print("Usage: python3 print_data_stats.py <data_dir>")
     exit()
local_dir = sys.argv[1]
print("print_type (e2e | udl1 | udl2 |udl3 | all):")
print_type = input().strip()

if print_type not in ["e2e", "udl1", "udl2", "udl3", "all"]:
     print("Invalid print_type")
     exit()
print("drop_warmup number:")
drop_warmup_num = int(input())

pd.set_option('display.max_columns', None)


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


def print_e2e_stats(df):
     duration_df = process_end_to_end_latency_dataframe(df, end_at_client=True)
     type_name="END-TO-END LATENCY"
     print("-------- ", type_name, " --------")
     print_duration_df(duration_df, column_name='e2e_latency')
     print("------------------------------------")
     duration_df.to_csv('debug.csv', index=False)
     throughput = compute_throughput(duration_df)
     print(f"Throughput: {throughput} Qps")

def print_udl1_stats(df):
     duration_df_dict = process_udl1_dataframe(df)
     print_udl_stats(duration_df_dict, "UDL1 CENTROIDS SEARCH")


def print_udl2_stats(df):
     duration_df_dict , batch_size_df= process_udl2_dataframe(df)
     # Note that deserialize_blob_time different because some blob contains more query sub-batches while others contain less
     print_udl_stats(duration_df_dict, "UDL2 CLUSTER SEARCH")
     print_duration_df(batch_size_df, 'batch_size')


def print_udl3_stats(df):
     duration_df_dict = process_udl3_dataframe(df)
     print_udl_stats(duration_df_dict, "UDL3 AGGREGATE (+ LLM GENERATE)")


def print_udls(df):
     duration_df_dict = {}
     duration_df_dict["e2e_latency"] = process_end_to_end_latency_dataframe(df)
     print_avgs(duration_df_dict, "END-TO-END LATENCY")
     duration_df_dict = process_udl1_dataframe(df)
     print_avgs(duration_df_dict, "UDL1 CENTROIDS SEARCH")
     duration_df_dict,_ = process_udl2_dataframe(df)
     print_avgs(duration_df_dict, "UDL2 CLUSTER SEARCH")
     duration_df_dict = process_udl3_dataframe(df)
     print_avgs(duration_df_dict, "UDL3 AGGREGATE (+ LLM GENERATE)")
     duration_df_dict = process_btw_udls(df)
     from_back_client_dict = process_from_back_client(df)
     duration_df_dict.update(from_back_client_dict)
     print_avgs(duration_df_dict, "BETWEEN UDLs")

log_files = get_log_files(local_dir, suffix)
log_data = get_log_files_dataframe(log_files)
df = clean_log_dataframe(log_data,drop_warmup=drop_warmup_num)

if print_type == "e2e":
     print_e2e_stats(df)
     
     
elif print_type == "udl1":
     print_udl1_stats(df)
     
elif print_type == "udl2":
     print_udl2_stats(df)

     
elif print_type == "udl3":
     print_udl3_stats(df)
     
elif print_type == "all":
     print_udls(df)
