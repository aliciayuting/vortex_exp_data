import matplotlib.pyplot as plt

import os
import sys
import re


throughput_data_pattern = r'Throughput with batch size ([0-9]+) \(([^\)]*)\): (.*)'

def read_throughput(fname):
    data = ([], [])
    units = ''
    with open(fname, 'r') as f:
        parts = f.read().split('\n\n')
        test_split_data = parts[0].split('\n')
        for line in test_split_data:
            matches = re.search(throughput_data_pattern, line)
            if matches:
                batch_size = matches.group(1)
                units = matches.group(2)
                throughput = matches.group(3)
                
                data[0].append(int(batch_size))
                data[1].append(float(throughput))
                
        f.close()
    return (data, units)
    

def plot_throughput_by_batch_size(title, in_fname, out_fname):
    data = read_throughput(in_fname)

    print(data)
    
    plt.plot(data[0][0], data[0][1])

    plt.title(title)
    plt.xlabel('Batch size')
    plt.ylabel('Throughput')

    plt.tight_layout()
    plt.savefig(out_fname)


plot_throughput_by_batch_size(sys.argv[1], sys.argv[2], sys.argv[3])
