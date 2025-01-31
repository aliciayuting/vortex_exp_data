import pandas as pd
import matplotlib.pyplot as plt
import sys

# provide CSV file and plot name as arguments 1 and 2 respectively

in_file = fname = sys.argv[1]

data = pd.read_csv(in_file, header=None)
data = data.values.flatten()
data = data // 1000

out_file = sys.argv[2]

plt.hist(data, bins=10, edgecolor='black')
plt.title(out_file)
plt.xlabel('Latency (μs)')
plt.ylabel('Frequency')
plt.savefig(f'{out_file}_plot_hist.png')
