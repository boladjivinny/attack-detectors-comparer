"""This modules puts together all the functions that provide a necessary
feature in running the comparison. It is basically a set of utilities
functions.
"""

import argparse

from ..algorithms import *
from ..processers import *


def get_objects_type(comparison_type) -> tuple:
    """Identifies the relevant classes to be used to run the comparison.

    This function uses the comparison type to identify the relevant
    algorithm and processing modules classes that are needed to perform
    the comparison. 

    Args:
        comparison_type (`str`): the type of comparison to be performed.

    Returns:
        tuple(Algorithm, Processer): the algorithm and the processer classes.

    Raises:
        `ValueError`: when the comparison type does not belong to the 
        accepted type.
    """
    if comparison_type == 'flow':
        return FlowBasedProcesser, Algorithm
    elif comparison_type == 'time':
        return TimeBasedProcesser, TimeBasedAlgorithm
    elif comparison_type == 'weight':
        return WeightBasedProcesser, WeightBasedAlgorithm

    # if not, raise an error
    raise ValueError('The corresponding type is not supported.')

def parse_args() -> argparse.Namespace:
    """Parses the command-line arguments passed to the module.

    This function sets the arguments that are expected from the program
    and parses them when the user runs the main script.

    Args:
        None

    Returns:
        `Namespace`: an object with all the arguments expected from the
        program.

    Raises:
        `argparse.ArgumentError`: when the values passed to the program
        are not of the type or length expected. Also, when a required 
        combination of arguments is not observed.
    """
    parser = argparse.ArgumentParser(
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
    parser.add_argument('-p', '--plot', choices=['TPR', 'TNR', 'FPR', 'FNR',
        'Precision', 'Accuracy', 'ErrorRate', 'FM1', 'FM2', 'FM05'], 
        help='defines the metric that should be plotted.', default=None)
    parser.add_argument('-a', '--alpha', type=float, default=0.01,
        help="in weight mode, use this alpha for computing the score")
    parser.add_argument('-c', '--csv', type=argparse.FileType('w+'),
        help="print the final scores in csv format into the specified file.")
    parser.add_argument('-o', '--out', type=argparse.FileType('w'),
        help="store in a log file everything that is shown in the screen.")
    parser.add_argument('-P', '--plot-to-file', type=str,
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

    if args.type in ["weight", "time"] and (args.time == 0):
        parser.error(f"[-t {args.type}] requires -T <time window>.")
    if len(args.labels) != 2:
        parser.error('--labels expects 2 values.')    

    return args
