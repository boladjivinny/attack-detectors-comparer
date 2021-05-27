#  Copyright (C) 2009  Sebastian Garcia, Martin Grill, Jan Stiborek
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
# 1.0 
#    Update the code to have a module architecture.
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

from os.path import basename, splitext
from os import dup2

from .utils import get_objects_type, parse_args

def main():
    args = parse_args()

    verbose = args.verbose
    file = args.file
    comparison_type = args.type
    time_window = args.time
    doplot = args.plot
    alpha = args.alpha
    csv_file = args.csv
    out_file = args.out
    plot_file = args.plot_to_file
    label = args.label
    dummy = args.generate_dummy_algos
    labels = args.labels
    predictions = args.predictions

    # create the processer
    import time
    s = time.time()
    cls_proc, cls_alg = get_objects_type(comparison_type)

    proc = cls_proc(label, labels)

    # create the algorithms

    data = pd.read_csv(
        file, 
        usecols=['StartTime', 'SrcAddr', label], parse_dates=[0])

    features = data.drop(columns=[label])

    # load the labels as "str" to make the processing easy

    baseline = cls_alg(
        "real", features, data[label].astype(str), labels, label
    )

    # methods
    algorithms = [
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

        e = time.time()
        print(f'setup completed in {e - s} seconds.')
            
        proc(baseline, *algorithms, window_size=time_window, alpha=alpha, verbose=verbose)
        proc.report_results(algorithms)
        if doplot:
            #plot(file, time_window, comparison_type, time_windows_group)
            pass

    except Exception as e:
            print("misc. exception (runtime error from user callback?):", e)
    except KeyboardInterrupt:
        # CTRL-C pretty handling.
        print("Keyboard Interruption!. Exiting.")
        exit(1)

if __name__ == '__main__':
    main()
