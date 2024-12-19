import csv
import matplotlib.pyplot as plt

input_file = 'gpu_utilization.dat'
gpu_trimmed_file = 'gpu_trimmed.dat'
mem_trimmed_file = 'gpu_mem_trimmed.dat'
gpu_plot_file = 'gpu_utilization_plot.png'
mem_plot_file = 'gpu_mem_utilization_plot.png'


def remove_columns_gpu():
    columns_to_remove = [2, 3, 4, 5]

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
    open(gpu_trimmed_file, mode='w', newline='', encoding='utf-8') as outfile:
        csv_reader = csv.reader(infile)
        csv_writer = csv.writer(outfile)

        for row in csv_reader:
            filtered_row = [value for index, value in enumerate(row) if index not in columns_to_remove]
            csv_writer.writerow(filtered_row)

    print(f"Columns removed and saved to {gpu_trimmed_file}")


def remove_columns_mem():
    columns_to_remove = [1, 3, 4, 5]

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
    open(mem_trimmed_file, mode='w', newline='', encoding='utf-8') as outfile:
        csv_reader = csv.reader(infile)
        csv_writer = csv.writer(outfile)

        for row in csv_reader:
            filtered_row = [value for index, value in enumerate(row) if index not in columns_to_remove]
            csv_writer.writerow(filtered_row)

    print(f"Columns removed and saved to {mem_trimmed_file}")


def plot_gpu():
    timestamps = []
    gpu_usage = []

    with open(gpu_trimmed_file, mode='r', newline='', encoding='utf-8') as infile:
        csv_reader = csv.reader(infile)
        for row in csv_reader:
            if len(row) != 2:
                continue

            timestamp_str, gpu_usage_str = row

            try:
                timestamp = int(timestamp_str)
                gpu_usage_str = gpu_usage_str.replace(' %', '')
                gpu_usage_value = float(gpu_usage_str)
            except ValueError:
                continue
            timestamps.append(timestamp)
            gpu_usage.append(gpu_usage_value)

    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, gpu_usage, label='GPU Usage', color='b')
    plt.xlabel('Time')
    plt.ylabel('GPU Usage (%)')
    plt.title('GPU Utilization Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(gpu_plot_file)
    plt.show()
    print(f"Plot saved to {gpu_plot_file}")


def plot_mem():
    timestamps = []
    mem_usage = []

    with open(mem_trimmed_file, mode='r', newline='', encoding='utf-8') as infile:
        csv_reader = csv.reader(infile)
        for row in csv_reader:
            if len(row) != 2:
                continue

            timestamp_str, mem_usage_str = row

            try:
                timestamp = int(timestamp_str)
                mem_usage_str = mem_usage_str.replace(' %', '')
                mem_usage_value = float(mem_usage_str)
            except ValueError:
                continue
            timestamps.append(timestamp)
            mem_usage.append(mem_usage_value)

    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, mem_usage, label='GPU Memory Usage', color='b')
    plt.xlabel('Time')
    plt.ylabel('MEM Usage (%)')
    plt.title('GPU Memory Utilization Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(mem_plot_file)
    plt.show()
    print(f"Plot saved to {mem_plot_file}")


if __name__ == "__main__":
    remove_columns_gpu()
    plot_gpu()
    remove_columns_mem()
    plot_mem()
