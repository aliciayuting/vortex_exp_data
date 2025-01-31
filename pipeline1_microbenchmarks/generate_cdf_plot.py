import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

import sys


# provide CSV file and plot name as arguments 1 and 2 respectively

times = pd.read_table(sys.argv[1], sep=',', header=None).transpose()
times.columns = ['latency']
times = times.drop([0]) # specify which trials to drop
times['latency'] //= 1000 # convert to microsecs

# write stats
mean = int(np.mean(times['latency']))
median = int(np.median(times['latency']))
percentile_95 = int(np.percentile(times['latency'], 95))

fname = sys.argv[2].lower().replace(' ', '_')
print(fname)

with open(f'{fname}_stats.csv', 'w') as f:
    f.write(f'mean,median,95th percentile\n{mean},{median},{percentile_95}')
    f.close()

# generate plot
sns.set_theme()
sns.kdeplot(data=times, x='latency', cumulative=True)
plt.xlabel('Latency (μs)')
plt.title(sys.argv[2])
plt.savefig(f'{fname}_plot.png')
