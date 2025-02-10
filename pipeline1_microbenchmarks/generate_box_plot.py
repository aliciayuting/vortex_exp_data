import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json

import sys
import os


data_root = sys.argv[1]
out_root = sys.argv[2]

data = []
with open('data.json', 'r') as f:
    segments = json.loads(f.read())
    for s in segments['segments']:
        if s['type'] == 'horizontal_csv':
            times = pd.read_table(os.path.join(data_root, s['file_name']), sep=',', header=None).transpose()
            times = times.iloc[segments['drop']:].reset_index(drop=True)
            times.columns = ['latency']
            times['latency'] //= 1000
            
            default = s['file_name'].split('.')[0] + '_box_plot.png'
            
            data.append((s['name'], times['latency'].to_numpy(), s['out'] if 'out' in s else default))
        elif s['type'] == 'csv':
            times = pd.read_csv(os.path.join(data_root, s['file_name']))
            times = times.iloc[segments['drop']:].reset_index(drop=True)
            for c in s['columns']:
                times[c['csv_name']] //= 1000
                default = s['file_name'].split('.')[0] + '_' + c['csv_name'] + '_box_plot.png'
                data.append((c['name'], times[c['csv_name']].to_numpy(), c['out'] if 'out' in c else default))
    f.close()


def annotate_stats(box, percentile_95, variance):
    box_dist = np.diff(plt.gca().get_xticks())[0]
    pad = box_dist / 10
    
    is_mean_less = box['means'][0].get_xydata()[0][0] < box['medians'][0].get_xydata()[0][0]
    
    for i, (elt, color) in enumerate([('means', 'green'), ('medians', 'orange')]):
        for line in box[elt]:
            (x, y_b), (_, y_t) = line.get_xydata()

            x_text = x
            if (is_mean_less and elt == 'means') or ((not is_mean_less) and elt == 'medians'):
                x_text -= pad
            else: x_text += pad
            
            plt.annotate(
                int(x) if elt == 'medians' else f'{x:.2f}',
                xy=(x, y_t),
                xytext=(x_text, y_t+0.05),
                horizontalalignment='center',
                arrowprops=dict(arrowstyle='-', lw=1.5),
                color=color
            )
            
    plt.annotate(f'Variance: {variance}\n95th percentile: {percentile_95}',xy=(0.01, 0.85), xycoords='axes fraction', fontsize=12)
    plt.legend(loc='upper left', fontsize=12, fancybox=True, framealpha=0.5, shadow=True, facecolor='white', handles=[box['means'][0]], labels=['Mean'])
    

for (n, d, dest) in data:
    plt.figure(figsize=(12, 7))
    
    box = plt.boxplot(d, vert=False, patch_artist=True, showfliers=False, showmeans=True, meanline=True)
    
    percentile_95 = int(np.percentile(d, 95))
    variance = int(np.var(d))
    
    annotate_stats(box, percentile_95, variance)
    
    plt.title(n, fontsize=15)
    plt.yticks([])
    plt.xlabel('Time (us)', fontsize=15)

    plt.tight_layout()
    plt.savefig(os.path.join(out_root, dest))
