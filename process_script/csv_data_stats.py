import pandas as pd
from process_data import *
import os
import pandas as pd
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")

def write_statistics_to_csv(sub_component_latencies, csv_filename):
     results = []
     for component, df in sub_component_latencies.items():
          if df.empty:
               continue
          avg_duration = int(round(df[component].mean()))
          mean_duration = int(round(df[component].mean()))
          std_duration = df[component].std() # for some timestamp, like emb_load time, there is only 1 entry, so std is NaN in such case
          std_duration = int(round(std_duration)) if not pd.isna(std_duration) else 0
          max_duration = int(round(df[component].max()))
          min_duration = int(round(df[component].min()))
          
          results.append({
               'component': component,
               'avg duration(us)': avg_duration,
               'mean duration(us)': mean_duration,
               'std duration': std_duration,
               'max duration(us)': max_duration,
               'min duration': min_duration
          })

     results_df = pd.DataFrame(results, columns=["component", "avg duration(us)", "mean duration(us)", "std duration", "max duration(us)", "min duration"])

     if not os.path.isfile(csv_filename):
          results_df.to_csv(csv_filename, index=False)
     else:
          results_df.to_csv(csv_filename, mode='a', header=False, index=False)




if __name__ == "__main__":
     arguments = sys.argv
     if len(sys.argv) < 3:
          print("Usage: python3 csv_data_stats.py <data_dir> <csv_dir>")
          exit()
     local_dir = sys.argv[1]
     csv_dir = sys.argv[2]

     log_files = get_log_files(local_dir, suffix)
     log_data = get_log_files_dataframe(log_files)
     df = clean_log_dataframe(log_data)

     name =  "breakdown_" + local_dir.split("/")[-1] + ".csv"
     csv_name = os.path.join(csv_dir, name)
     if os.path.exists(csv_name):
          os.remove(csv_name)

     
     e2e_duration_df_dict = {}
     e2e_duration_df_dict['e2e_latency'] = process_end_to_end_latency_dataframe(df)
     write_statistics_to_csv(e2e_duration_df_dict, csv_name)
     udl1_duration_df_dict = process_encode_centroids_search_udl_dataframe(df)
     write_statistics_to_csv(udl1_duration_df_dict, csv_name)
     udl2_duration_df_dict = process_cluster_search_udl_dataframe(df)
     write_statistics_to_csv(udl2_duration_df_dict, csv_name)
     udl3_duration_df_dict = process_agg_generate_udl_dataframe(df)
     write_statistics_to_csv(udl3_duration_df_dict, csv_name)
     
     
