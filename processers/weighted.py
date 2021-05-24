from .time_based import TimeBasedProcesser
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score
from sklearn.metrics import f1_score, fbeta_score
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
        print(f'alpha={alpha}, id={tw_id}, first_sum={FIRST_SUM}, second_sum={SECOND_SUM}, cf={correcting_function}')
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
