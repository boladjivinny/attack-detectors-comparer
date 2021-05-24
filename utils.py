import argparse

from .algorithms import *
from .processers import *


def get_objects_type(comparison_type):
    if comparison_type == 'flow':
        return FlowBasedProcesser, Algorithm
    elif comparison_type == 'time':
        return TimeBasedProcesser, TimeBasedAlgorithm
    elif comparison_type == 'weight':
        return WeightBasedProcesser, WeightBasedAlgorithm

    # if not, raise an error
    raise ValueError('The corresponding type is not supported.')

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
    parser.add_argument('-t', '--type', choices=["flow", "time", "weight"],
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
        help="store in a log file everything that is shown in the screen.")
    parser.add_argument('-P', '--plot-to-file', type=argparse.FileType('w'),
        help="instead of showing the plot on the screen, store it in a file."\
            "Type of plot given by the file extension.")
    parser.add_argument('-l', '--label', type=str, default='Label',
        help="the title of the column representing the label field.")
    parser.add_argument('-L', '--labels', type=str, nargs='+', 
        help="the labels available in the dataset (i.e. negative, positive,"\
            " and optionally, background labels", default=['normal', 'botnet'])
    parser.add_argument('-g', '--generate-dummy-algos', action='store_true',
        help='whether to create the AllPositive and AllNegative'\
             'algorithms.')
    parser.add_argument('file', metavar="input", type=argparse.FileType('r'),
        help="sorted input netflow labeled file to analyze "\
            "(Netflow or Argus).")
    parser.add_argument('predictions', help="the prediction files for each"\
        " of the methods being evaluated", nargs="+",
        type=argparse.FileType('r'))

    args = parser.parse_args()

    if args.type in ["weighted", "time"] and (args.time == 0):
        parser.error(f"[-t {args.type}] requires -T <time window>.")
    if len(args.labels) != 2:
        parser.error('--labels expects 2 values.')
    

    return args