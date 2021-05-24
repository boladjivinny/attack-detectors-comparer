from .time_based import TimeBasedProcesser
import math

FIRST_SUM = 0
SECOND_SUM = 1

class WeightBasedProcesser(TimeBasedProcesser):
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
            algo.weighted_current_reportprint("AllPositive")
        print()
        print('+ Cumulative Weighted +')
        for algo in algos:
            algo.weighted_reportprint("AllPositive")
        print()
