import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import re
import json

warnings.filterwarnings("ignore")

suffix = ".dat"

MULTIPLIER = 100000

def get_dfg_file(local_dir):
     os.path.join(local_dir, "dfgs.json.tmp")
     return os.path.join(local_dir, "dfgs.json.tmp")

def get_dfg_information(dfg_file):
     information = {}
     with open(dfg_file) as f:
          dfg_data = json.load(f)
     information['top_num_centroids'] = dfg_data[0]["graph"][0]["user_defined_logic_config_list"][0]["top_num_centroids"]
     return information


def get_log_files(local_dir, suffix):
     log_files = []
     for root, dirs, files in os.walk(local_dir):
          for file in files:
               if file[-4:] == suffix:
                    file_path = os.path.join(root, file)
                    log_files.append(file_path)
     return log_files


def get_log_files_dataframe(log_files):
     log_data = []
     for log_file_path in log_files:
          df = pd.read_csv(log_file_path, 
                         delim_whitespace=True, 
                         comment='#', 
                         names=["tag", "timestamp", "node_id", "querybatch_id", "cluster_id", "extra"],
                         header=None)
          log_data.append(df)
     combined_df = pd.concat(log_data, ignore_index=True)
     return combined_df


def get_gpu_log_files(local_dir, suffix):
     log_files = []
     for root, dirs, files in os.walk(local_dir):
          for file in files:
               if file[-4:] == suffix and "gpu" in file:
                    file_path = os.path.join(root, file)
                    log_files.append(file_path)
     return log_files

def trim_df(df, start_loc, end_loc):
     df = df.iloc[start_loc:end_loc]
     return df

def clean_log_dataframe(log_data, drop_warmup=30):
     df = pd.DataFrame(log_data, columns=["tag", "timestamp", "node_id", "querybatch_id","cluster_id", "extra"])
     df = df.drop(columns=['extra'])
     df['tag'] = df['tag'].astype(int)
     df['node_id'] = df['node_id'].astype(int)
     df['timestamp'] = df['timestamp'].astype(int)
     df['timestamp'] = df['timestamp']/1000 # convert to microseconds
     df['querybatch_id'] = df['querybatch_id'].astype(int)
     df['cluster_id'] = df['cluster_id'].astype(int)
     df = df[df['querybatch_id'] >= drop_warmup ]
     
     # drop df with 'querybatch_id' btween MULTIPLIER to MULTIPLIER*drop_warmup
     df = df[~((df['tag'].between(40000, 50000)) & (df['querybatch_id'] // MULTIPLIER < drop_warmup))]
     df[df['querybatch_id'] == 250 ].to_csv('querybatch_250.csv', index=False)
     return df



def get_durations(df, start_tag, end_tag, group_by_columns=['node_id'], duration_name='latency'):
     filtered_df = df[(df['tag'] == start_tag) | (df['tag'] == end_tag)]
     grouped = filtered_df.groupby(group_by_columns)['timestamp']
     duration_results = []
     for group_values, timestamps in grouped:
          latency = timestamps.max() - timestamps.min()
          if len(group_by_columns) > 1:
               result = {group_by_column: value for group_by_column, value in zip(group_by_columns, group_values)}
               result[duration_name] = latency
               duration_results.append(result)
          else:
               duration_results.append({group_by_columns[0]: group_values, duration_name: latency})
     duration_df = pd.DataFrame(duration_results)
     # print(f"{duration_name} duration size",len(duration_df))
     return duration_df


def get_durations_based_on_nodes(df, start_tag, end_tag, group_by_columns=['node_id'], duration_name='latency'):
    filtered_df = df[(df['tag'] == start_tag) | (df['tag'] == end_tag)]
    grouped = filtered_df.groupby(group_by_columns)[['timestamp', 'node_id']]
    same_node_durations = []
    different_node_durations = []
    
    for group_values, data in grouped:
        if data['node_id'].nunique() == 1:
            latency = data['timestamp'].max() - data['timestamp'].min()
            result = {group_by_column: value for group_by_column, value in zip(group_by_columns, group_values)}
            result[duration_name+"_same_node_time"] = latency
            same_node_durations.append(result)
        else:
            latency = data['timestamp'].max() - data['timestamp'].min()
          #   latency = end_time - start_time
            result = {group_by_column: value for group_by_column, value in zip(group_by_columns, group_values)}
            result[duration_name+"_diff_nodes_time"] = latency
            different_node_durations.append(result)
    
    same_node_df = pd.DataFrame(same_node_durations)
    different_node_df = pd.DataFrame(different_node_durations)
#     print(different_node_df)
    return same_node_df, different_node_df

def process_e2e_dataframe(df):
     sub_component_latencies = {}
     sub_component_latencies['e2e_time'] = get_durations(df, 40100, 10000, group_by_columns=['node_id'], duration_name='e2e_time')
     return sub_component_latencies

def process_last_udl_dataframe(df):
     sub_component_latencies = {}
     sub_component_latencies['last_udl_time'] = get_durations(df, 40100, 40000, group_by_columns=['node_id'], duration_name='last_udl_time')
     return sub_component_latencies

# def process_udl1_dataframe(df):
#      sub_component_latencies = {}
#      sub_component_latencies['udl1_time'] = get_durations(df, 20000, 20100, group_by_columns=['node_id','querybatch_id'], duration_name='udl1_time')
#      sub_component_latencies['centroids_load_time'] = get_durations(df, 20010, 20011, group_by_columns=['node_id'], duration_name='centroids_load_time')
#      sub_component_latencies['get_embeddings_time'] = get_durations(df, 20020, 20021, group_by_columns=['node_id','querybatch_id'], duration_name='get_embeddings_time')
#      sub_component_latencies['centroids_search_time'] = get_durations(df, 20030, 20031, group_by_columns=['node_id','querybatch_id'], duration_name='centroids_search_time')     
#      sub_component_latencies['combine_same_centroids_time'] = get_durations(df, 20031, 20041, group_by_columns=['node_id','querybatch_id'], duration_name='combine_same_centroids_time')
#      return sub_component_latencies

# def process_udl2_dataframe(df):
#      sub_component_latencies = {}
#      sub_component_latencies['udl2_time'] = get_durations(df, 30000, 30050, group_by_columns=['node_id','querybatch_id','cluster_id'], duration_name='udl2_time')
#      sub_component_latencies['load_cluster_embs_time'] = get_durations(df, 30010, 30011, group_by_columns=['node_id','cluster_id'], duration_name='load_cluster_embs_time')
#      sub_component_latencies['deserialize_blob_time'] = get_durations(df, 30020, 30021, group_by_columns=['node_id','querybatch_id','cluster_id'], duration_name='deserialize_blob_time')
#      sub_component_latencies['add_to_batch_time'] = get_durations(df, 30021, 30022, group_by_columns=['node_id','querybatch_id','cluster_id'], duration_name='add_to_batch_time')
#      # sub_component_latencies['cluster_emb_search_time'] = get_durations(df, 30030, 30031, group_by_columns=['node_id','querybatch_id','cluster_id'], duration_name='cluster_emb_search_time')
#      # sub_component_latencies['construct_new_keys_emb_time'] = get_durations(df, 30031, 30041, group_by_columns=['node_id','querybatch_id','cluster_id'], duration_name='construct_new_keys_emb_time')
#      sub_component_latencies['batch_search_time'] = get_durations(df, 30030, 30031, group_by_columns=['node_id','querybatch_id','cluster_id'], duration_name='batch_search_time')
#      batch_size_df = df[(df['tag']==30032)]
#      batch_size_df = batch_size_df.rename(columns={'node_id': 'batch_size'})
#      return sub_component_latencies, batch_size_df


# def process_udl3_dataframe(df):
#      sub_component_latencies = {}
#      udl3_df = df[(df['tag'] >= 40000) & (df['tag'] < 50000)]
#      # NOTE: qb_qid = query_batch_id * MULTIPLIER * QUERY_PER_BATCH + qid 
#      udl3_df['batch_id'] = (udl3_df['querybatch_id'] // MULTIPLIER).astype(int)
#      udl3_df['qid'] = (udl3_df['querybatch_id'] % MULTIPLIER).astype(int)
#      udl3_df[udl3_df['batch_id'] == 250 ].to_csv('3querybatch_250.csv', index=False)
#      sub_component_latencies['udl3_time'] = get_durations(udl3_df, 40000, 40030, group_by_columns=['node_id','batch_id','qid'], duration_name='udl3_time')
#      sub_component_latencies['parse_blob_time'] = get_durations(udl3_df, 40000, 40001, group_by_columns=['node_id','batch_id','qid','cluster_id'], duration_name='parse_blob_time')
#      # sub_component_latencies['check_not_fully_gather_time'] = get_durations(udl3_df, 40001, 40010, group_by_columns=['node_id','batch_id','qid','cluster_id'], duration_name='check_not_fully_gather_time')
#      sub_component_latencies['query_finish_gather_time'] = get_durations(udl3_df, 40000, 40020, group_by_columns=['node_id','batch_id','qid'], duration_name='query_finish_gather_time')
#      sub_component_latencies['retrieve_doc_time'] = get_durations(udl3_df, 40020, 40021, group_by_columns=['node_id','batch_id','qid'], duration_name='retrieve_doc_time')
#      sub_component_latencies['llm_generate_time'] = get_durations(udl3_df, 40021, 40030, group_by_columns=['querybatch_id'], duration_name='llm_generate_time')
#      # sub_component_latencies['result_put_time'] = get_durations(udl3_df, 40030, 40031, group_by_columns=['node_id','batch_id','qid'], duration_name='result_put_time')
#      return sub_component_latencies

# def process_btw_udls(df):
#      sub_component_latencies = {}
#      # NOTE: qb_qid = query_batch_id * MULTIPLIER * QUERY_PER_BATCH + qid 
#      df.loc[df['tag'] == 40000, 'querybatch_id'] = (df.loc[df['tag'] == 40000, 'querybatch_id'] // MULTIPLIER).astype(int)
#      df.columns = [col.replace("querybatch_id", "batch_id") for col in df.columns]
#      sub_component_latencies['udl1_udl2_time'] = get_durations(df, 20050, 30000, group_by_columns=['node_id','batch_id','cluster_id'], duration_name='udl1_udl2_time')
#      sub_component_latencies['udl2_udl3_time'] = get_durations(df, 30050, 40000, group_by_columns=['node_id','batch_id','cluster_id'], duration_name='udl2_udl3_time')
#      return sub_component_latencies


# def process_btw_udls_nodes(df):
#      sub_component_latencies = {}
#      df.loc[df['tag'] == 40000, 'querybatch_id'] = (df.loc[df['tag'] == 40000, 'querybatch_id'] // MULTIPLIER).astype(int)
#      df.columns = [col.replace("querybatch_id", "batch_id") for col in df.columns]
#      same_node_df, diff_nodes_df = get_durations_based_on_nodes(df, 20050, 30000, group_by_columns=['batch_id','cluster_id'], duration_name='udl1_udl2')
#      sub_component_latencies['udl1_udl2_same_node_time'] = same_node_df
#      sub_component_latencies['udl1_udl2_diff_nodes_time'] = diff_nodes_df
#      # same_node_df2, diff_nodes_df2 = get_durations_based_on_nodes(df, 30050, 40000, group_by_columns=['batch_id','cluster_id'], duration_name='udl2_udl3')
#      # sub_component_latencies['udl2_udl3_same_node_time'] = same_node_df2
#      # sub_component_latencies['udl2_udl3_diff_nodes_time'] = diff_nodes_df2
#      return sub_component_latencies



# def process_from_back_client(df):
#      sub_component_latencies = {}
#      df.columns = [col.replace("querybatch_id", "batch_id") for col in df.columns]
#      sub_component_latencies['from_client_time'] = get_durations(df, 10000, 20000, group_by_columns=['node_id','batch_id'], duration_name='from_client_time')
#      # TODO: change it to handle batch > 1 case, there the group_by_columns should be ['node_id','querybatch_id','cluster_id']
#      df.loc[df['tag'] == 40030, 'batch_id'] = (df.loc[df['tag'] == 40030, 'batch_id'] // MULTIPLIER).astype(int)
#      sub_component_latencies['back_client_time'] = get_durations(df, 40030, 10100, group_by_columns=['node_id','batch_id'], duration_name='back_client_time')
#      return sub_component_latencies
     

# def process_end_to_end_latency_dataframe(original_df, end_at_client=True):
#      # # tag 10000 is the input send time, 40031 is the time when agg_udl finished put the result to cascade
#      end_tag = 40031 if not end_at_client else 10100
     
#      filtered_df = original_df[original_df['tag'].isin([10000, end_tag])]
#      df = filtered_df.rename(columns={
#                     'tag': 'tag',
#                     'timestamp': 'timestamp',
#                     'node_id': 'client_id',
#                     'querybatch_id': 'batch_id',
#                     'cluster_id': 'qid'
#                     })
#      start_df = df[df['tag'] == 10000].groupby(['client_id', 'batch_id','qid']).first().reset_index()
#      df['batch_id'] = df.apply(
#           lambda row: int(row['batch_id'] // MULTIPLIER) if row['tag'] == 40031 else row['batch_id'],
#           axis=1
#      )
#      end_df = df[df['tag'] == end_tag].groupby(['client_id', 'batch_id','qid']).first().reset_index()
#      latency_df = pd.merge(
#         end_df, 
#         start_df, 
#         on=['client_id', 'batch_id','qid'], 
#         suffixes=('_end', '_start')
#     )
#      latency_df['e2e_latency'] = latency_df['timestamp_end'] - latency_df['timestamp_start']
#      # result_count = len(latency_df)
#      # unique_count = len(latency_df.drop_duplicates())
#      # print(f"Number of rows:{result_count} \nNumber of unique (client_id, batch_id, qid) combinations: {unique_count}")
#      return latency_df

# def compute_throughput(df):
#      start_time = df['timestamp_start'].min()
#      end_time = df['timestamp_end'].max()
#      total_time = round((end_time - start_time) / 1000000.0 , 3 )# convert to seconds
#      total_queries = len(df)
#      throughput = total_queries / total_time
#      return throughput

