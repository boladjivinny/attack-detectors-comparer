#  Copyright (C) 2021  Vinny Adjibi
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# Author:
# Vinny Adjibi <vinny AT cmu DOT edu>, <vinny.adjibi AT outlook DOT com>
#
# Changelog
# 1.0  Sun 30 May 2021 11:19:55 AM CAT
#    + Updated the code to be executed with a modular architecture
#    + Code reformatted for work with Python3
#    + Allows users to plot any of the error metrics
#    + Removes the background processing
#
# 0.8  Thu Nov  7 09:47:52 UTC 2013
#       Read the format of the biargus complete weblogs
# 0.7
#       Add the option to store the plot in a file, also to store all the resuls in a file.
# 0.6
#       Added the new time-weighted measure
#       t-TP, t-FN, t-TN, t-FP, t-Precision, t-Recall, TMeasure
#       And a lot of more stuff...
# 0.5
#       I added the fmeasure 0.5
#       Now the plot is correctly done
#       
# 0.4 
#     29 Oct 2012
#    We added counters for the background labels too. 
#        B1 is when the predicted label was negative, and the real label was background.
#        B2 is when the predicted label was positive, and the real label was background.
#        B3 is when the predicted label was background, and the real label was negative.
#        B4 is when the predicted label was background, and the real label was positive.
#        B5 is when the predicted label was background, and the real label was background.
# 0.3 
#     Oct 9 2012
#       Changed ...
# 0.2 
#     Ago 2 2012
#       Added support for plotting the fmeasures.
#     Ago 1 2012
#       Added Fmeasure2 in the output
#     Jul 30 2012
#     Added support for time based comparison of flows.
# 0.1 dic 8 2011
#       First version

import sys

import pandas as pd
import matplotlib.pyplot as plt

from os.path import basename, splitext
from os import dup2

from .utils import get_objects_type, parse_args

def main():
    args = parse_args()

    verbose = args.verbose
    file = args.file
    comparison_type = args.type
    time_window = args.time
    plot_metric = args.plot
    alpha = args.alpha
    csv_file = args.csv
    out_file = args.out
    plot_file = args.plot_to_file
    label = args.label
    dummy = args.generate_dummy_algos
    labels = args.labels
    predictions = args.predictions

    # create the processer
    cls_proc, cls_alg = get_objects_type(comparison_type)

    proc = cls_proc(label, labels)

    # create the algorithms. Only the relevant columns are loaded

    data = pd.read_csv(
        file, 
        usecols=['StartTime', 'SrcAddr', label], parse_dates=[0])

    features = data.drop(columns=[label])

    # load the labels as "str" to make the processing easy

    algorithms = [cls_alg(
        "real", features, data[label].astype(str), labels, label
    )]

    # methods
    algorithms += [
        cls_alg(
            splitext(basename(f.name))[0], 
            None, 
            f.read().splitlines(), labels, label
        )
        for f in predictions
    ]

    if dummy:
        names = ['AllNegative', 'AllPositive']
        algorithms += [
            cls_alg(
                name, None, 
                [labels[i]] * data.shape[0], labels, label
            )
            for i, name in enumerate(names)
        ]

    try:
        if out_file is not None:
            dup2(out_file.fileno(), sys.stdout.fileno())
            dup2(out_file.fileno(), sys.stderr.fileno())

        proc(*algorithms, window_size=time_window, alpha=alpha, verbose=verbose)
        proc.report_results(algorithms[1:])
        if plot_metric:
            if comparison_type == 'flow':
                # fix names for FM
                metric = plot_metric.replace('FM', 'fmeasure')
                plt.plot(
                    [algo.name for algo in algorithms[1:]],
                    [100 * getattr(algo, metric) for algo in algorithms[1:]]
                )
                plt.legend([metric])
                plt.title(f"Comparison of {metric} for the different techniques")
                plt.xlabel("Detection technique")
                plt.ylabel("%")
            else:
                # get the values for each algorithm
                results = {algo.name: getattr(algo, f'r{plot_metric}') for algo in algorithms[1:]}
                df = pd.DataFrame(results)
                df.plot(xlabel='Timeframe', ylabel='%', title=f"Evolution of the {plot_metric} over the timeframes ({time_window}s)")
            if plot_file:
                plt.savefig(plot_file)
            else:
                plt.show()
        # saving final results to a CSV file if available
        if csv_file:
            header = 'Name,TP,TN,FP,FN,TPR,TNR,FPR,FNR,Precision,Accuracy,ErrorRate,fmeasure1,fmeasure2,fmeasure05\n'
            text = '\n'.join([algo.csv_reportprint() for algo in algorithms[1:]])
            csv_file.write(f'{header}{text}')
            csv_file.close()

    except Exception as e:
            print("misc. exception (runtime error from user callback?):", e)
    except KeyboardInterrupt:
        # CTRL-C pretty handling.
        print("Keyboard Interruption!. Exiting.")
        exit(1)

if __name__ == '__main__':
    main()
