import matplotlib.pyplot as plt
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import numpy as np
from process_data import *
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import matplotlib.patches as mpatches


def plot_bar_breakdown(data, labels, save_file_name, break1_start=100000, break1_end=475000, break2_start=600000, break2_end=1754000):
     # Calculate average duration for each component in `data`
     avg_durations = [np.mean(times) for times in data]
     start_times = [0]
     for duration in avg_durations[:-1]:
          start_times.append(start_times[-1] + duration)

     # Compute the end time for each component
     end_times = [start + duration for start, duration in zip(start_times, avg_durations)]
     print(f"start_times: {start_times}")
     print(f"end_times: {end_times}")

     # Calculate break points based on data
     break1_start = 10000
     break1_end = int((end_times[1] - 1000) / 1000) * 1000
     break2_start = int((end_times[1] + 10000) / 1000) * 1000
     break2_end = int((end_times[6] - 10000) / 10000) * 10000 + 2000
     print(f"break1_start: {break1_start}, break1_end: {break1_end}, break2_start: {break2_start}, break2_end: {break2_end}")

     # Assign colors for each label
     colors = plt.cm.tab20.colors  # Use color map for variety

     fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 4), sharey=True, gridspec_kw={'width_ratios': [1, 1, 1], 'wspace': 0.05})

     # Set x-limits based on actual time ranges
     ax1.set_xlim(0, break1_start)
     ax2.set_xlim(break1_end, break2_start)
     ax3.set_xlim(break2_end, end_times[-1])

     # Set custom tick intervals for ax3 to be every 2000 units
     ticks = np.arange(break2_end, end_times[-1] + 1, 2000)

     ax3.set_xticks(ticks)
     ax3.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x)}"))  # Format tick labels as integers
     
     tick_labels = [f"{int(tick)}" if idx != 0 else "" for idx, tick in enumerate(ticks)]
     ax3.set_xticklabels(tick_labels)

     # Track plotted labels for a custom legend
     legend_patches = {}

     # Plot each component on the appropriate axes with two x-axis breaks
     for idx, (label, start, end, duration) in enumerate(zip(labels, start_times, end_times, avg_durations)):
          color = colors[idx % len(colors)]  # Cycle colors if more than 20

          # Add the label to legend_patches only if it hasn't been added before
          if label not in legend_patches:
               legend_patches[label] = mpatches.Patch(color=color, label=label)

          # Case 1: Component is entirely before the first break
          if end <= break1_start:
               ax1.broken_barh([(start, duration)], (0, 0.8), facecolors=color)
          
          # Case 2: Component is entirely between the first and second breaks
          elif start >= break1_end and end <= break2_start:
               ax2.broken_barh([(start, duration)], (0, 0.8), facecolors=color)

          # Case 3: Component is entirely after the second break
          elif start >= break2_end:
               ax3.broken_barh([(start, duration)], (0, 0.8), facecolors=color)

          # Case 4: Component spans the first break (split between ax1 and ax2)
          elif start < break1_start < end <= break2_start:
               duration_before_break1 = break1_start - start
               ax1.broken_barh([(start, duration_before_break1)], (0, 0.8), facecolors=color)
               
               duration_after_break1 = end - break1_end
               ax2.broken_barh([(break1_end, duration_after_break1)], (0, 0.8), facecolors=color)

          # Case 5: Component spans the second break (split between ax2 and ax3)
          elif start >= break1_end and start < break2_start < end:
               duration_before_break2 = break2_start - start
               ax2.broken_barh([(start, duration_before_break2)], (0, 0.8), facecolors=color)
               
               duration_after_break2 = end - break2_end
               ax3.broken_barh([(break2_end, duration_after_break2)], (0, 0.8), facecolors=color)

     # Customize subplots to remove y-axis elements and add break markers
     for ax in [ax1, ax2, ax3]:
          ax.set_yticklabels([])  # Remove y-axis labels
          ax.tick_params(left=False)  # Hide y-axis ticks

     # Add break markers between ax1 & ax2 and between ax2 & ax3
     d = 0.015  # Diagonal marker size for breaks
     kwargs = dict(color='k', clip_on=False)

     # Break markers between ax1 and ax2
     ax1.plot((1 - d, 1 + d), (-d, +d), transform=ax1.transAxes, **kwargs)
     ax1.plot((1 - d, 1 + d), (1 - d, 1 + d), transform=ax1.transAxes, **kwargs)
     ax2.plot((-d, +d), (-d, +d), transform=ax2.transAxes, **kwargs)
     ax2.plot((-d, +d), (1 - d, 1 + d), transform=ax2.transAxes, **kwargs)

     # Break markers between ax2 and ax3
     ax2.plot((1 - d, 1 + d), (-d, +d), transform=ax2.transAxes, **kwargs)
     ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), transform=ax2.transAxes, **kwargs)
     ax3.plot((-d, +d), (-d, +d), transform=ax3.transAxes, **kwargs)
     ax3.plot((-d, +d), (1 - d, 1 + d), transform=ax3.transAxes, **kwargs)

     # Add labels and title
     fig.supxlabel("Time (us)")
     fig.suptitle("Vortex RAG LLM End-to-End Latency Breakdown (Adjusted for Long Components)")

     # Create a legend using the custom patches
     fig.legend(handles=list(legend_patches.values()), loc="lower right", bbox_to_anchor=(0.85, 0.1), bbox_transform=fig.transFigure)

     # Save the plot
     plt.tight_layout()
     plt.savefig(save_file_name, format='pdf')
     plt.show()
     plt.close()


if __name__ == "__main__":
     arguments = sys.argv
     if len(sys.argv) < 3:
          print("Usage: python3 dot_plot_data.py <data_dir> <save_dir> ")
          exit()
     local_dir = sys.argv[1]
     save_dir = sys.argv[2]
     print("drop_warmup number:")
     drop_warmup_num = int(input())
     
     dfg_file = get_dfg_file(local_dir)
     dfg_info = get_dfg_information(dfg_file)
     print(f"num of centroids {dfg_info['top_num_centroids']}")
       
     log_files = get_log_files(local_dir, suffix)
     log_data = get_log_files_dataframe(log_files)
     df = clean_log_dataframe(log_data,drop_warmup=drop_warmup_num)

     from_back_client_times = process_from_back_client(df.copy()) 
     bt_udls_times = process_btw_udls(df.copy())

     start_to_udl1_times = from_back_client_times['from_client_time']['from_client_time']
     
     udl1_df = process_udl1_dataframe(df)
     udl1_times = udl1_df['udl1_time']['udl1_time']
     # Encoder time if enabled
     get_embeddings_times = udl1_df['get_embeddings_time']['get_embeddings_time']
     centroids_searchtimes = udl1_df['centroids_search_time']['centroids_search_time']
     udl1_2_times = bt_udls_times['udl1_udl2_time']['udl1_udl2_time']
   
     udl2_df,_ = process_udl2_dataframe(df)
     udl2_times = udl2_df['udl2_time']['udl2_time']
     batch_search_times = udl2_df['batch_search_time']['batch_search_time']
     udl2_3_times = bt_udls_times['udl2_udl3_time']['udl2_udl3_time']
     
     udl3_df = process_udl3_dataframe(df)
     udl3_times = udl3_df['udl3_time']['udl3_time']
     llm_times = udl3_df['llm_generate_time']['llm_generate_time']
     
     udl3_to_end_times = from_back_client_times['back_client_time']['back_client_time']    

     end_to_end_latency = process_end_to_end_latency_dataframe(df)["e2e_latency"]
     
     labels = [
          "Aggregator-UDL1",
          "UDL1:Encoder_time",
          "UDL1:Centroids_search_time",
          "UDL1-UDL2",
          "UDL2:batchSearch",
          "UDL2-UDL3",
          "UDL3:LLM_generate",
          "UDL3-End"
          # "End-to-End Latency"   
     ]
     data = [
          start_to_udl1_times,
          get_embeddings_times,
          centroids_searchtimes,
          udl1_2_times,
          batch_search_times,
          udl2_3_times,
          llm_times,
          udl3_to_end_times
          # end_to_end_latency
     ]
 
     plot_name = "bar_breakdown_plot" + local_dir.split("/")[-1] +".pdf"
     save_file_dir = os.path.join(save_dir, plot_name)
     plot_bar_breakdown(data, labels, save_file_name=save_file_dir)