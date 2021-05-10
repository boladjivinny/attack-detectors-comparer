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


import os
import sys
import argparse
import pandas as pd
import numpy as np

from . import *
from .utils import *
from .processers import FlowBasedProcesser, TimeBasedProcesser, WeightBasedProcesser
from .algorithms import Algorithm, TimeBasedAlgorithm, WeightBasedAlgorithm

def parse_args():
    parser = argparse.ArgumentParser(
        prog="BotnetDetectorsComparer",
        description='''
            This program is free software; you can
            redistribute it and/or modify it under the terms 
            of the GNU General Public License as published
            by the Free Software Foundation; either version
            2 of the License, or (at your option) any later 
            version.
        ''',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-v', '--verbose', action="count", 
        help="verbosity level", default=0)
    parser.add_argument('-D', '--debug', action='store_true', 
        help="debug. In debug mode the statistics run live.")
    parser.add_argument('-t', '--type', choices=["flow", "time", "weighted"],
        help="type of comparison. Flow based (-t flow), time based (-t time)"\
            ", or weighted (-t weight).", default="flow")
    parser.add_argument('-T', '--time', type=int, help="while using time "\
        "based comparison, specify the time window to use in seconds.",
        default=0)
    parser.add_argument('-p', '--plot', action="store_true", 
        help="plot the fmeasures of all methods.")
    parser.add_argument('-a', '--alpha', type=float, default=0.4,
        help="in weight mode, use this alpha for computing the score")
    parser.add_argument('-c', '--csv', type=argparse.FileType('w'),
        help="print the final scores in csv format into the specified file.")
    parser.add_argument('-o', '--out', type=argparse.FileType('w'),
        default=sys.stdout, help="store in a log file everything that is"\
             " shown in the screen.")
    parser.add_argument('-P', '--plot-to-file', type=argparse.FileType('w'),
        help="instead of showing the plot on the screen, store it in a file."\
            "Type of plot given by the file extension.")
    parser.add_argument('-l', '--label', type=str, default='Label',
        help="the title of the column representing the label field.")
    parser.add_argument('-L', '--labels', type=str, nargs='+', 
        help="the labels available in the dataset (i.e. negative, positive,"\
            " and optionally, background labels", default=['normal', 'botnet'])
    parser.add_argument('-B', '--background', action='store_true',
        help='whether the metrics for background traffic should be '\
        'considered')
    parser.add_argument('file', metavar="input", type=argparse.FileType('r'),
        help="sorted input netflow labeled file to analyze "\
            "(Netflow or Argus).")
    parser.add_argument('predictions', help="the prediction files for each"\
        " of the methods being evaluated", nargs="+",
        type=argparse.FileType('r'))

    args = parser.parse_args()

    if args.type in ["weighted", "time"] and (args.time == 0):
        parser.error(f"[-t {args.type}] requires -T <time window>.")
    if not (2 <= len(args.labels) <= 3):
        parser.error('--labels expects 2 or 3 values')
    # if background, we need three labels
    if (args.background and len(args.labels) !=3):
        parser.error('--background or -B requires at least 3 labels.')
    

    return args

def main():
    args = parse_args()

    verbose = args.verbose
    debug = args.debug or verbose > 0
    file = args.file
    comparison_type = args.type
    time_window = args.time
    doplot = args.plot
    alpha = args.alpha
    csv_file = args.csv
    out_file = args.out
    plot_file = args.plot_to_file
    label = args.label
    background = args.background
    labels = args.labels

    # create the processer
    pp = FlowBasedProcesser("Label", labels)
    tt = TimeBasedProcesser("Label", labels)
    ww = WeightBasedProcesser("Label", labels)

    data = pd.read_csv(file, usecols=['StartTime', 'SrcAddr', label], parse_dates=[0])

    algo1 = Algorithm("real", data.drop(columns=['Label']), data['Label'], labels)
    algo2 = TimeBasedAlgorithm("AllPositive", data.drop(columns=['Label']), np.array(['botnet'] * data.shape[0]), labels)

    algo2 = WeightBasedAlgorithm("AllPositive", data.drop(columns=['Label']), np.array(['botnet'] * data.shape[0]), labels)
    algo3 = WeightBasedAlgorithm("AllNegative", data.drop(columns=['Label']), np.array(['normal'] * data.shape[0]), labels)

    #pp(algo1, algo2)

    ww(time_window, algo1, algo2, algo3, alpha=alpha)
    #pp(algo1, algo2)
    ww.report_results([algo2, algo3])

    # create the algo

    # try:
    #     try:
    #         if (out_file != sys.stdout):
    #             os.dup2(out_file.fileno(), sys.stdout.fileno())
    #             os.dup2(out_file.fileno(), sys.stderr.fileno())
            
    #         process_file(file, comparison_type, time_window)
    #         if doplot:
    #             plot(file, time_window, comparison_type, time_windows_group)

    #     except Exception as e:
    #             print("misc. exception (runtime error from user callback?):", e)
    #     except KeyboardInterrupt:
    #             sys.exit(1)


    # except KeyboardInterrupt:
    #     # CTRL-C pretty handling.
    #     print("Keyboard Interruption!. Exiting.")
    #     sys.exit(1)


if __name__ == '__main__':
    main()
