from .base import BaseProcesser
from sklearn.metrics import confusion_matrix

class FlowBasedProcesser(BaseProcesser):
    """The processing module for a flow-by-flow comparison.

    This module compares the techniques using a flow-by-flow
    prediction strategy.

    Attributes:
        label_column (`str`): the name of the column of the labels.
        labels (`list`): the expected labels for the comparison.
    """
    # the arguments should be the techniques
    def __init__(self, label_column, labels):
        self.label_column = label_column
        self.labels = labels


    def __call__(self, *args, window_size=None, alpha=None, verbose=0):
        # here we need to compare the results
        self.get_longest_name_length(*args[1:])
        data = args[0].data

        label_dict = {k: i for i, k in enumerate(self.labels)}

        for algo in args:
            data[algo.name] = [
                label_dict[x] for x in algo.data[self.label_column]
            ]

        for algo in args[1:]:
            algo.TN, algo.FP, algo.FN, algo.TP = confusion_matrix(
                data[args[0].name], data[algo.name], labels=[0, 1]).ravel()
            algo.computeMetrics()