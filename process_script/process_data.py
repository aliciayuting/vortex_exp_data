import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import re

warnings.filterwarnings("ignore")

suffix = ".dat"


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
     return duration_df

def process_udl1_dataframe(df):
     sub_component_latencies = {}
     sub_component_latencies['udl1_time'] = get_durations(df, 20000, 20100, group_by_columns=['node_id','querybatch_id'], duration_name='udl1_time')
     sub_component_latencies['centroids_load_time'] = get_durations(df, 20010, 20011, group_by_columns=['node_id'], duration_name='centroids_load_time')
     sub_component_latencies['deserialize_blob_time'] = get_durations(df, 20020, 20021, group_by_columns=['node_id','querybatch_id'], duration_name='deserialize_blob_time')
     sub_component_latencies['centroids_search_time'] = get_durations(df, 20030, 20031, group_by_columns=['node_id','querybatch_id'], duration_name='centroids_search_time')     
     sub_component_latencies['combine_same_centroids_time'] = get_durations(df, 20031, 20041, group_by_columns=['node_id','querybatch_id'], duration_name='combine_same_centroids_time')
     sub_component_latencies['emit_next_udl_time'] = get_durations(df, 20050, 20051, group_by_columns=['node_id','querybatch_id','cluster_id'], duration_name='emit_next_udl_time')
     return sub_component_latencies

def process_udl2_dataframe(df):
     sub_component_latencies = {}
     sub_component_latencies['udl2_time'] = get_durations(df, 30000, 30100, group_by_columns=['node_id','querybatch_id','cluster_id'], duration_name='udl2_time')
     sub_component_latencies['load_cluster_embs_time'] = get_durations(df, 30010, 30011, group_by_columns=['node_id','cluster_id'], duration_name='load_cluster_embs_time')
     sub_component_latencies['deserialize_blob_time'] = get_durations(df, 30020, 30021, group_by_columns=['node_id','querybatch_id','cluster_id'], duration_name='deserialize_blob_time')
     sub_component_latencies['cluster_emb_search_time'] = get_durations(df, 30021, 30031, group_by_columns=['node_id','querybatch_id','cluster_id'], duration_name='cluster_emb_search_time')
     sub_component_latencies['construct_new_keys_emb_time'] = get_durations(df, 30031, 30041, group_by_columns=['node_id','querybatch_id','cluster_id'], duration_name='construct_new_keys_emb_time')
     # missing next blob serialize time, if needed, add it to the loggings in code base
     emit_df = get_durations(df, 30050, 30051, group_by_columns=['node_id','querybatch_id','cluster_id'], duration_name='emit_next_udl_time')
     emit_df.rename(columns={'node_id':'client_id','querybatch_id':'querybatch_id', 'cluster_id':'qid', 'emit_next_udl_time':'emit_next_udl_time'}, inplace=True)
     sub_component_latencies['emit_next_udl_time'] = emit_df
     return sub_component_latencies

def process_udl3_dataframe(df):
     sub_component_latencies = {}
     udl3_df = df[(df['tag'] >= 40000) & (df['tag'] < 50000)]
     # NOTE: qb_qid = query_batch_id * 100000 * QUERY_PER_BATCH + qid 
     multiplier = 100000
     udl3_df['batch_id'] = (udl3_df['querybatch_id'] // multiplier).astype(int)
     udl3_df['qid'] = (udl3_df['querybatch_id'] % multiplier).astype(int)
     
     sub_component_latencies['udl3_time'] = get_durations(udl3_df, 40000, 40031, group_by_columns=['node_id','batch_id','qid'], duration_name='udl3_time')
     sub_component_latencies['parse_blob_time'] = get_durations(udl3_df, 40000, 40001, group_by_columns=['node_id','batch_id','qid','cluster_id'], duration_name='parse_blob_time')
     # sub_component_latencies['check_not_fully_gather_time'] = get_durations(udl3_df, 40001, 40010, group_by_columns=['node_id','batch_id','qid','cluster_id'], duration_name='check_not_fully_gather_time')
     sub_component_latencies['query_finish_gather_time'] = get_durations(udl3_df, 40000, 40020, group_by_columns=['node_id','batch_id','qid'], duration_name='query_finish_gather_time')
     sub_component_latencies['retrieve_doc_time'] = get_durations(udl3_df, 40020, 40021, group_by_columns=['node_id','batch_id','qid'], duration_name='retrieve_doc_time')
     # sub_component_latencies['disk_load_answer_table_time'] = get_durations(udl3_df, 40120, 40121, group_by_columns=['node_id','cluster_id'], duration_name='disk_load_answer_table_time')
     # sub_component_latencies['disk_load_doc_time'] = get_durations(udl3_df, 40220, 40221, group_by_columns=['node_id','cluster_id'], duration_name='disk_load_doc_time')
     # TODO: could also add a dump json timestamp here
     # sub_component_latencies['llm_generate_time'] = get_durations(udl3_df, 40021, 40030, group_by_columns=['querybatch_id'], duration_name='llm_generate_time')
     sub_component_latencies['result_put_time'] = get_durations(udl3_df, 40030, 40031, group_by_columns=['node_id','batch_id','qid'], duration_name='result_put_time')
     return sub_component_latencies


def process_end_to_end_latency_dataframe(original_df, end_at_client=False):
     # # tag 10000 is the input send time, 40031 is the time when agg_udl finished put the result to cascade
     end_tag = 40031
     if end_at_client:
          end_tag = 10100
     filtered_df = original_df[original_df['tag'].isin([10000, end_tag])]
     df = filtered_df.rename(columns={
                    'tag': 'tag',
                    'timestamp': 'timestamp',
                    'node_id': 'client_id',
                    'querybatch_id': 'batch_id',
                    'cluster_id': 'qid'
                    })
     start_timestamp = df[df['tag'] == 10000].set_index(['client_id', 'batch_id'])['timestamp']
     df['batch_id'] = df.apply(
          lambda row: int(row['batch_id'] // 100000) if row['tag'] == 40031 else row['batch_id'],
          axis=1
     )
     df = df.merge(start_timestamp, on=['client_id', 'batch_id'], suffixes=('', '_start'))
     df['e2e_latency'] = df['timestamp'] - df['timestamp_start']
     df_queries = df[df['tag'] == end_tag]
     result_df = df_queries[['client_id', 'batch_id', 'qid', 'e2e_latency']]
     result_count = len(result_df)
     unique_combinations = result_df[['client_id', 'batch_id', 'qid']].drop_duplicates()
     unique_count = len(unique_combinations)
     print(f"Number of rows:{result_count} \nNumber of unique (client_id, batch_id, qid) combinations: {unique_count}")
     return result_df


