import csv
import matplotlib.pyplot as plt
from collections import defaultdict

input_file = 'gpu_by_process.dat'
trimmed_file = 'gpu_by_process_trimmed.dat'
mem_plot_file = 'gpu_mem_utilization_by_process.png'


''' 
The input file 'gpu_by_process.dat' contains fields 'unix_time',
'process_name', 'pid', 'used_memory'. 
Generates an output file including only fields 'unix_time', 'pid',
'used_memory'.
'''
def remove_columns():
    columns_to_remove = [1]

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
    open(trimmed_file, mode='w', newline='', encoding='utf-8') as outfile:
        csv_reader = csv.reader(infile)
        csv_writer = csv.writer(outfile)

        for row in csv_reader:
            filtered_row = [value for index, value in enumerate(row) if index not in columns_to_remove]
            csv_writer.writerow(filtered_row)

    print(f"Columns removed and saved to {trimmed_file}")


'''
Plots per-process GPU memory utilization over time.
'''
def plot_gpu_memory():
    process_data = defaultdict(list)

    with open(trimmed_file, mode='r', newline='', encoding='utf-8') as infile:
        csv_reader = csv.reader(infile)
        for row in csv_reader:
            if len(row) != 3:
                continue

            timestamp_str, process_id_str, gpu_mem_str = row

            try:
                timestamp = int(timestamp_str)
                process_id = int(process_id_str)
                gpu_mem_str = gpu_mem_str.replace(' MiB', '')
                gpu_mem_value = float(gpu_mem_str)
            except ValueError:
                continue
            process_data[process_id].append((timestamp, gpu_mem_str))

    plt.figure(figsize=(10, 6))

    for process_id, data in process_data.items():
        timestamps, gpu_mem_usages = zip(*sorted(data, key=lambda x: x[0]))
        plt.plot(timestamps, gpu_mem_usages, label=f'Process {process_id}')

    plt.xlabel('Time')
    plt.ylabel('GPU Memory Usage (MiB)')
    plt.title('Per Process GPU Memory Utilization Over Time')
    plt.legend(title="Processes", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(mem_plot_file)
    plt.show()

    print(f"Plot saved to {mem_plot_file}")


if __name__ == "__main__":
    remove_columns()
    plot_gpu_memory()
