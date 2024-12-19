import csv
import matplotlib.pyplot as plt
from collections import defaultdict

input_file = 'cpu_utilization.dat'
cpu_trimmed_file = 'cpu_trimmed.dat'
mem_trimmed_file = 'mem_trimmed.dat'
cpu_plot_file = 'cpu_utilization_plot.png'
mem_plot_file = 'mem_utilization_plot.png'


def remove_columns_cpu():
    columns_to_remove = [2, 3, 4, 5, 6, 7, 8, 10, 11, 12]

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
    open(cpu_trimmed_file, mode='w', newline='', encoding='utf-8') as outfile:
        csv_reader = csv.reader(infile)
        csv_writer = csv.writer(outfile)

        for row in csv_reader:
            filtered_row = [value for index, value in enumerate(row) if index not in columns_to_remove]
            csv_writer.writerow(filtered_row)

    print(f"Columns removed and saved to {cpu_trimmed_file}")


def remove_columns_mem():
    columns_to_remove = [2, 3, 4, 5, 6, 7, 8, 9, 11, 12]

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
    open(mem_trimmed_file, mode='w', newline='', encoding='utf-8') as outfile:
        csv_reader = csv.reader(infile)
        csv_writer = csv.writer(outfile)

        for row in csv_reader:
            filtered_row = [value for index, value in enumerate(row) if index not in columns_to_remove]
            csv_writer.writerow(filtered_row)

    print(f"Columns removed and saved to {mem_trimmed_file}")


def plot_cpu():
    process_data = defaultdict(list)

    with open(cpu_trimmed_file, mode='r', newline='', encoding='utf-8') as infile:
        csv_reader = csv.reader(infile)
        for row in csv_reader:
            if len(row) != 3:
                continue

            timestamp_str, process_id_str, cpu_usage_str = row

            try:
                timestamp = int(timestamp_str)
                process_id = int(process_id_str)
                cpu_usage = float(cpu_usage_str)
            except ValueError:
                continue
            process_data[process_id].append((timestamp, cpu_usage))

    plt.figure(figsize=(10, 6))

    for process_id, data in process_data.items():
        timestamps, cpu_usages = zip(*sorted(data, key=lambda x: x[0]))
        plt.plot(timestamps, cpu_usages, label=f'Process {process_id}')

    plt.xlabel('Time')
    plt.ylabel('CPU Usage (%)')
    plt.title('Per Process CPU Utilization Over Time')
    plt.legend(title="Processes", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(cpu_plot_file)
    plt.show()

    print(f"Plot saved to {cpu_plot_file}")


def plot_mem():
    process_data = defaultdict(list)

    with open(mem_trimmed_file, mode='r', newline='', encoding='utf-8') as infile:
        csv_reader = csv.reader(infile)
        for row in csv_reader:
            if len(row) != 3:
                continue

            timestamp_str, process_id_str, mem_usage_str = row

            try:
                timestamp = int(timestamp_str)
                process_id = int(process_id_str)
                mem_usage = float(mem_usage_str)
            except ValueError:
                continue
            process_data[process_id].append((timestamp, mem_usage))

    plt.figure(figsize=(10, 6))

    for process_id, data in process_data.items():
        timestamps, mem_usages = zip(*sorted(data, key=lambda x: x[0]))
        plt.plot(timestamps, mem_usages, label=f'Process {process_id}')

    plt.xlabel('Time')
    plt.ylabel('MEM Usage (%)')
    plt.title('Per Process Memory Utilization Over Time')
    plt.legend(title="Processes", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(mem_plot_file)
    plt.show()

    print(f"Plot saved to {mem_plot_file}")


if __name__ == "__main__":
    remove_columns_cpu()
    plot_cpu()
    remove_columns_mem()
    plot_mem()
