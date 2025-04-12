import sys
import os
import warnings
from process_data import *

warnings.filterwarnings("ignore")


def filter_query_related_rows(df, qb_id):
     multiplier = 100000
     filtered_df = df[(df['querybatch_id'] == qb_id) |
                 ((df['querybatch_id'] >= qb_id * multiplier) & (df['querybatch_id'] < (qb_id + 1) * multiplier))]
     min_timestamp = filtered_df['timestamp'].min()
     filtered_df['timestamp'] = filtered_df['timestamp'] - min_timestamp
     df_sorted = filtered_df.sort_values(by='timestamp', ascending=True)
     return df_sorted


if __name__ == "__main__":
     arguments = sys.argv
     if len(sys.argv) < 3:
          print("Usage: python3 trace_one_query.py <data_dir> <save_dir> ")
          exit()
     local_dir = sys.argv[1]
     save_dir = sys.argv[2]
     print("querybatch_id:")
     qb_id = input().strip()
     try:
          qb_id = int(qb_id)
          name =  "trace_query_num" + str(qb_id) + local_dir.split("/")[-1] + ".csv"
          save_file_name = os.path.join(save_dir, name)

          log_files = get_log_files(local_dir, suffix)
          log_data = get_log_files_dataframe(log_files)
          df = clean_log_dataframe(log_data)
          qb_df = filter_query_related_rows(df, qb_id)
          qb_df.to_csv(save_file_name, index=False)
     except ValueError:
          print("Invalid query number")
          exit()
     
     
     

     


