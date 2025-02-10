import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json

import sys
import os


data_root = sys.argv[1]
out_root = sys.argv[2]

data = []
bar_groups = []
with open('data.json', 'r') as f:
    segments = json.loads(f.read())
    for group in segments['bars']:
        data.append({'name': group['name'], 'data': []})
        for bar in group['data']:
            if bar['type'] == 'horizontal_csv':
                times = pd.read_table(os.path.join(data_root, bar['file_name']), sep=',', header=None).transpose()
                times = times.iloc[segments['drop']:].reset_index(drop=True)
                times.columns = ['latency']
                times['latency'] //= 1000
                
                if bar['bar_group'] not in bar_groups:
                    bar_groups.append(bar['bar_group'])
                
                data[-1]['data'].append((bar['bar_group'], times['latency'].to_numpy()))
            elif bar['type'] == 'csv':
                times = pd.read_csv(os.path.join(data_root, bar['file_name']))
                times = times.iloc[segments['drop']:].reset_index(drop=True)
                for c in bar['columns']:
                    times[c['csv_name']] //= 1000
                    
                    if c['bar_group'] not in bar_groups:
                        bar_groups.append(c['bar_group'])
                    
                    data[-1]['data'].append((c['bar_group'], times[c['csv_name']].to_numpy()))
    f.close()


bars_by_group = { group: [[],[],[]] for group in bar_groups  }
for i, group in enumerate(data):
    acc_y = 0
    for bar in group['data']:
        height = np.median(bar[1])
        bars_by_group[bar[0]][0].append(i)
        bars_by_group[bar[0]][1].append(height)
        bars_by_group[bar[0]][2].append(acc_y)
        acc_y += height



colors = ['red', 'orange', 'blue', 'yellow', 'green']

plt.figure(figsize=(8, 7))

for i, group in enumerate(bar_groups):
    plt.bar(
        bars_by_group[group][0],
        bars_by_group[group][1],
        color=colors[i],
        bottom=bars_by_group[group][2],
        width=0.5
    )

plt.title('Latency Breakdown', fontsize=15)
plt.xticks([i for i in range(len(data))], labels=[group['name'] for group in data])
plt.ylabel('Time (us)', fontsize=15)
plt.legend(bar_groups)

plt.tight_layout()
plt.savefig(os.path.join(out_root, 'latency_breakdown_bar_plot.png'))
