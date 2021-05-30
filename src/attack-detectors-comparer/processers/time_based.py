from ..algorithms.base import Algorithm
import datetime

from .base import BaseProcesser
from sklearn.metrics import confusion_matrix


class TimeBasedProcesser(BaseProcesser):
    """The processing module for a flow-by-flow comparison.

    This module compares the techniques using time windows
    and the occurence of IPs both in the normal and malicious
    classes.

    Attributes:
        label_column (`str`): the name of the column of the labels.
        labels (`list`): the expected labels for the comparison.
    """
    def __init__(self, label_column, labels):
        self.label_column = label_column
        self.labels = labels

    def __call__(self, *args, window_size=None, alpha=None, verbose=0):

        def get_error_message(name, ip, label, prediction):
            msg = f' > Computing errors for algorithm: '\
                f'{name}. Ip: {ip}. Real label: {label}. '\
                f'Predicted label: {prediction}'
            # assuming they come in as integer
            if label == self.labels[0]: # normal
                # TN
                if prediction == label:
                    msg = f'{msg}\n\tReal Label: \x1b\x5b1;33;40m{label}'\
                    f'\x1b\x5b0;0;40m, {name}: {prediction}. '\
                    f'Decision \x1b\x5b1;33;40mTN\x1b\x5b0;0;40m'
                else:
                # FP
                    msg = f'{msg}\n\tReal Label: \x1b\x5b1;31;40m{label}'\
                    f'\x1b\x5b0;0;40m, {name}: {prediction}. '\
                    f'Decision \x1b\x5b1;31;40mFP\x1b\x5b0;0;40m'
            elif label == self.labels[1]: # botnet
                if prediction == label:
                    msg = f'{msg}\n\tReal Label: \x1b\x5b1;33;40m{label}'\
                    f'\x1b\x5b0;0;40m, {name}: {prediction}. '\
                    f'Decision \x1b\x5b1;33;40mTP\x1b\x5b0;0;40m'
                else:
                    msg = f'{msg}\n\tReal Label: \x1b\x5b1;33;40m{label}'\
                    f'\x1b\x5b0;0;40m, {name}: {prediction}. '\
                    f'Decision \x1b\x5b1;31;40mFN\x1b\x5b0;0;40m'
            return msg

        self.get_longest_name_length(*args[1:])
        data = args[0].data

        label_dict = {k: i for i, k in enumerate(self.labels)}

        algo_names = [*map(lambda algo: algo.name, args)]
        for algo in args:
            data[algo.name] = [
                label_dict[x] for x in algo.data[self.label_column]
            ]

        window = 0
        remaining = data.shape[0]

        # initialize the start time
        start_time = data['StartTime'].min()

        while (remaining > 0):
            end_time = start_time + datetime.timedelta(seconds=window_size)
            chunk = data.loc[
                (data['StartTime'] >= start_time) & 
                (data['StartTime'] < end_time)
            ]
            start_time = data.loc[
                data['StartTime'] >= end_time, 'StartTime'].min()
            remaining -= len(chunk)
            window += 1
            # now the labels for each algorithm and we compared
            grouped = chunk.groupby('SrcAddr')
            technique_labels = grouped[algo_names].agg(max)

            true_y = technique_labels[args[0].name].tolist()
            true_labels = [self.labels[x] for x in true_y]
            if verbose > 0:
                print("####################################")
                print(f'Time Window Number: {window}')
                print(f'Amount of algorithms being used: {len(args)-1}')
                ips_report = {
                    ll: true_y.count(i) 
                    for i, ll in enumerate(self.labels)
                }
                print(f'Amount of unique ips: {ips_report}')
                labels_report = dict(chunk[self.label_column].value_counts())
                print(f'Amount of labels: {labels_report}')
                print(f'Lines read: {chunk.shape[0]}')
                print('####################################')
                print()


            for algo in args[1:]:
                y = technique_labels[algo.name]
                labels = [self.labels[x] for x in y]
                # display errors
                if verbose > 1:
                    print(
                        '\n'.join(
                            [
                                get_error_message(
                                    algo.name, ip, label, prediction)
                                for (ip, _), label, prediction in 
                                zip(grouped, true_labels, labels)]
                        )
                    )
                
                algo.cTN, algo.cFP, algo.cFN, algo.cTP = confusion_matrix(
                    true_y, y, labels=[0, 1]).ravel()
                self._process_time_window(true_labels, algo, window, alpha)
            
            if verbose > 0:
                self._show_reports(*args[1:])
    
    def _process_time_window(
        self, y_true: list, algo: Algorithm, 
        tw_id: int, alpha=None
        ) -> None:
        """Performs the necessary computation and other steps needed for each
        algorithm and time window.

        Args:
            y_true (`list`): the true labels for the time window.
            algo: (`Algorithm`): the detection technique being processed.
            tw_id (`int`): the time window's ID.
            alpha (`alpha`): the value of alpha used for computing the
                correcting function.

        Returns:
            None
        """
        algo.computeMetrics()
        algo.logMetrics()

    def _show_reports(self, *algos) -> None:
        """Prints the current metrics for all the detection techniques.

        This method outputs all the relevant metrics for the detection
        technique upon the time window is processed.

        Args:
            algos (`list`): the list of algorithms.

        Returns:
            None
        """
        print('+ Current Errors +')
        for algo in algos:
            algo.current_reportprint(self.max_name_length)
        print()
