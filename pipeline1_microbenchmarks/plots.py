import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def plot_cdf(times, title, out_name, unit):
    mean = round(np.mean(times), 2)
    median = round(np.median(times), 2)
    percentile_95 = round(np.percentile(times, 95), 2)
    variance = round(np.var(times), 2)

    sns.set_theme()
    sns.kdeplot(data=times, cumulative=True)
    plt.xlabel(f'Latency ({unit})')
    plt.title(title)
    plt.annotate(f'Mean: {mean}\nMedian: {median}\nVariance: {variance}\n95th percentile: {percentile_95}',xy=(0.6, 0.05), xycoords='axes fraction', fontsize=12)
    plt.savefig(f'{out_name}_cdf_plot.png')


def plot_hist(times, title, out_name, unit):
    mean = round(np.mean(times), 2)
    median = round(np.median(times), 2)
    percentile_95 = round(np.percentile(times, 95), 2)
    variance = round(np.var(times), 2)

    plt.hist(times, bins=10, edgecolor='black')
    plt.title(title)
    plt.xlabel(f'Latency ({unit})')
    plt.ylabel('Frequency')
    plt.annotate(f'Mean: {mean}\nMedian: {median}\nVariance: {variance}\n95th percentile: {percentile_95}',xy=(0.65, 0.8), xycoords='axes fraction', fontsize=10)
    plt.savefig(f'{out_name}_hist_plot.png')


def _annotate_stats_box(box, percentile_95, variance):
    box_dist = np.diff(plt.gca().get_xticks())[0]
    pad = box_dist / 8
    
    is_mean_less = box['means'][0].get_xydata()[0][0] < box['medians'][0].get_xydata()[0][0]
    
    for i, (elt, color) in enumerate([('means', 'green'), ('medians', 'orange')]):
        for line in box[elt]:
            (x, y_b), (_, y_t) = line.get_xydata()

            x_text = x
            if (is_mean_less and elt == 'means') or ((not is_mean_less) and elt == 'medians'):
                x_text -= pad
            else: x_text += pad
            
            plt.annotate(
                f'{x:.2f}',
                xy=(x, y_t),
                xytext=(x_text, y_t+0.05),
                horizontalalignment='center',
                arrowprops=dict(arrowstyle='-', lw=1.5),
                color=color
            )
            
    plt.annotate(f'Variance: {variance}\n95th percentile: {percentile_95}',xy=(0.01, 0.85), xycoords='axes fraction', fontsize=12)
    plt.legend(loc='upper left', fontsize=12, fancybox=True, framealpha=0.5, shadow=True, facecolor='white', handles=[box['means'][0]], labels=['Mean'])
    

def plot_box(times, title, out_name, unit):
    plt.figure(figsize=(12, 7))
    
    box = plt.boxplot(times, vert=False, patch_artist=True, showfliers=False, showmeans=True, meanline=True)
    
    percentile_95 = round(np.percentile(times, 95), 2)
    variance = round(np.var(times), 2)
    
    _annotate_stats_box(box, percentile_95, variance)
    
    plt.title(title, fontsize=15)
    plt.yticks([])
    plt.xlabel(f'Latency ({unit})', fontsize=15)

    plt.tight_layout()
    plt.savefig(f'{out_name}_box_plot.png')
