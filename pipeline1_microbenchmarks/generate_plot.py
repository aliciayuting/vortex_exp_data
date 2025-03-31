import sys
import os
import argparse

import pandas as pd
import numpy as np

from plots import *


def read_hcsv(fname, drops):
    times = pd.read_table(fname, sep=',', header=None).transpose()
    times.columns = ['latency']
    times = times.drop(np.arange(drops))
    return times['latency']


def read_hcsv_row(fname, row_name, drops):
    df = pd.read_csv(fname, header=None)
    df = df[df[0] == row_name]\
        .drop(0, axis=1)\
        .transpose()\
        .reset_index(drop=True)\
        .drop(np.arange(drops))\
        .reset_index(drop=True)
    df.columns = ['latency']
    return df['latency']

parser = argparse.ArgumentParser()

parser.add_argument('in_fname', type=str)
parser.add_argument('-p', '--plot-type', type=str)
parser.add_argument('-o', '--out', type=str, help='Output path')
parser.add_argument('-r', '--row-name', type=str, help='CSV row name')
parser.add_argument('-d', '--drop-count', type=int, help='# trials to drop from the top')
parser.add_argument('-t', '--title', type=str, help='Plot title')

args = parser.parse_args()

fname = args.in_fname
ptype = args.plot_type

drops = args.drop_count if args.drop_count else 0
data = read_hcsv_row(fname, args.row_name, drops) if args.row_name else read_hcsv(fname, drops)
unit = 'us'

if np.median(data) > 5000000000:
    data //= 1000
    data /= 1000000
    unit = 's'
elif np.median(data) > 5000000:
    data //= 1000
    data /= 1000
    unit = 'ms'
else:
    data //= 1000

out_name = args.out if args.out else fname.split('/')[-1].split('.')[0]
pretty = args.title if args.title else out_name.replace('_', ' ').title()

if ptype == 'cdf':
    plot_cdf(data, pretty, out_name, unit)
elif ptype == 'hist':
    plot_hist(data, pretty, out_name, unit)
elif ptype == 'box':
    plot_box(data, pretty, out_name, unit)