import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from process_data import *

warnings.filterwarnings("ignore")

arguments = sys.argv
if len(sys.argv) < 2:
     print("Usage: python3 print_data_stats.py <data_dir> <print_type>(e2e_latency | udl1 | udl2 | udl3)\n\
           udl1 is the encoder + centroids search \n\
           udl2 is the cluster search \n\
           udl3 is the aggregate + LLM generate \n\
           default <print_type>: e2e_latency")
     exit()
local_dir = sys.argv[1]
print_type = "e2e_latency"
if len(sys.argv) > 2:
     print_type = sys.argv[2]

pd.set_option('display.max_columns', None)


def print_e2e_stats(df):
     duration_df = process_end_to_end_latency_dataframe(df)
     print("-------- END-TO-END LATENCY --------")
     print("number of batch_query counts: ", duration_df['querybatch_id'].count())
     print("average e2e latency (us): ", duration_df['e2e_latency'].mean())
     print("median e2e latency (us): ", duration_df['e2e_latency'].median())
     print("max e2e latency (us): ", duration_df['e2e_latency'].max())
     print("min e2e latency (us): ", duration_df['e2e_latency'].min())
     print("standard deviation: ", duration_df['e2e_latency'].std())
     print("------------------------------------")


def print_udl1_stats(df):
     duration_df_dict = process_encode_centroids_search_udl_dataframe(df)


def print_udl2_stats(df):
     duration_df_dict = process_cluster_search_udl_dataframe(df)
     # Note that deserialize_blob_time different because some blob contains more query sub-batches while others contain less

def print_udl3_stats(df):
     duration_df_dict = process_agg_generate_udl_dataframe(df)

log_files = get_log_files(local_dir, suffix)
log_data = get_log_files_dataframe(log_files)
df = clean_log_dataframe(log_data)


if print_type == "e2e_latency":
     print_e2e_stats(df)
     
elif print_type == "udl1":
     print_udl1_stats(df)
     
elif print_type == "udl2":
     print_udl2_stats(df)
     
elif print_type == "udl3":
     print_udl3_stats(df)
