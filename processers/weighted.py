from .time_based import TimeBasedProcesser
import math

FIRST_SUM = 0
SECOND_SUM = 1

class WeightBasedProcesser(TimeBasedProcesser):
    """The processing module for a flow-by-flow comparison.

    This module compares the techniques using time windows
    and the occurence of IPs both in the normal and malicious
    classes. Weights are also used to favor earlier detection.

    Attributes:
        label_column (`str`): the name of the column of the labels.
        labels (`list`): the expected labels for the comparison.
    """
    def _process_time_window(self, y_true, algo, tw_id, alpha):
        # call the parent
        super()._process_time_window(y_true, algo, tw_id)
        # then compute weighted metrics
        correcting_function = math.exp(-alpha * (
            tw_id + FIRST_SUM)) + SECOND_SUM
        algo.compute_weighted_metrics(correcting_function, y_true)

    def _show_reports(self, *algos):
        super()._show_reports(*algos)
        print('+ Current Weighted +')
        for algo in algos:
            algo.weighted_current_reportprint(self.max_name_length)
        print()
        print('+ Cumulative Weighted +')
        for algo in algos:
            algo.weighted_reportprint(self.max_name_length)
        print()

    def report_results(self, algos, common_title='Cumulative Common errors'):
        super().report_results(algos, common_title)
        print('Weighted errors')
        print('---------------')
        for algo in algos:
            algo.weighted_reportprint(self.max_name_length)
