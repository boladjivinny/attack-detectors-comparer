import datetime
import time

from .base import BaseProcesser
from sklearn.metrics import confusion_matrix

class TimeBasedProcesser(BaseProcesser):
    # the arguments should be the techniques
    def __init__(self, label_column, labels):
        self.label_column = label_column
        self.labels = labels

    def __call__(self, *args, window_size=None, alpha=None, verbose=0):
        data = args[0].data
        #data['Timeframe'] = -1

        for algo in args:
            data[algo.name] = algo.data[self.label_column]
        window = 0
        processed = 0

        # initialize the start time
        start_time = data['StartTime'].min()

        while (processed < data.shape[0]):
            print(f"Time window: {window + 1}")
            s = time.time()
            end_time = start_time + datetime.timedelta(seconds=window_size)
            chunk = data.loc[(data['StartTime'] >= start_time) & (data['StartTime'] < end_time)]
            start_time = data.loc[data['StartTime'] >= end_time, 'StartTime'].min()
            
            #remainder = data.loc[data.Timeframe == -1]
            ##start_time = remainder['StartTime'].min()
            #chunk = remainder.loc[(remainder.StartTime >= start_time) & (remainder.StartTime < start_time + datetime.timedelta(seconds=window_size))]
            #data.loc[chunk.index, 'Timeframe'] = window
            processed += chunk.shape[0]
            window += 1
            data_by_ip = chunk.groupby('SrcAddr')
            e = time.time()

            print(f'collected the required information in {e - s} seconds.')

            true_y = None
            # now the labels for each algorithm and we compared
            ips = chunk.SrcAddr.unique()
            s = time.time()
            technique_labels = map(lambda algo: list(map(lambda s: int(self.labels[1] in s[1][algo.name].tolist()), data_by_ip)), args)
            e = time.time()
            print(f"Average of { (e - s) / len(args) } seconds.")
            for algo, y in zip(args, technique_labels):
                if true_y is None:
                    # reference is expected to be the first one
                    true_y = y

                    if verbose > 0:
                        print("####################################")
                        print(f'Time Window Number: {window}')
                        print(f'Amount of algorithms being used: {len(args)}')
                        ips_report = {ll: true_y.count(i) for i, ll in enumerate(self.labels)}
                        print(f'Amount of unique ips: {ips_report}')
                        labels_report = dict(chunk[self.label_column].value_counts())
                        print(f'Amount of labels: {labels_report}')
                        print(f'Lines read: {chunk.shape[0]}')
                        print('####################################')
                        print()
                    continue

                # display errors
                if verbose > 1:
                    for addr, ty, py in zip(ips, true_y, y):
                        print (f' > Computing errors for algorithm: '\
                        f'{algo.name}. Ip: {addr}. Real label: {ty}. '\
                        f'Predicted label: {py}')
                        if ty == self.labels[0]: # normal
                            # TN
                            if py == ty:
                                print (f'\tReal Label: \x1b\x5b1;33;40m{ty}'\
                                f'\x1b\x5b0;0;40m, {algo.name}: {py}. '\
                                f'Decision \x1b\x5b1;33;40mTN\x1b\x5b0;0;40m')
                            else:
                            # FP
                                print (f'\tReal Label: \x1b\x5b1;31;40m{ty}'\
                                f'\x1b\x5b0;0;40m, {algo.name}: {py}. '\
                                f'Decision \x1b\x5b1;31;40mFP\x1b\x5b0;0;40m')
                        elif ty == self.labels[1]: # botnet
                            if py == ty:
                                print (f'\tReal Label: \x1b\x5b1;33;40m{ty}'\
                                f'\x1b\x5b0;0;40m, {algo.name}: {py}. '\
                                f'Decision \x1b\x5b1;33;40mTP\x1b\x5b0;0;40m')
                            else:
                                print (f'\tReal Label: \x1b\x5b1;33;40m{ty}'\
                                f'\x1b\x5b0;0;40m, {algo.name}: {py}. '\
                                f'Decision \x1b\x5b1;31;40mFN\x1b\x5b0;0;40m')

                s = time.time()
                algo.cTN, algo.cFP, algo.cFN, algo.cTP = confusion_matrix(
                    true_y, y, labels=[0, 1]).ravel()
                prediction = list(map(lambda x: self.labels[x], true_y))
                self._process_time_window(prediction, algo, window, alpha)
                e = time.time()
                print(f'computed the metrics for {algo.name} in  {e - s} seconds.')
            
            if verbose > 0:
                self._show_reports(*args[1:])


    def _get_label(self, series):
        # series is a tuple, (used internally)
        return len([self.labels[0]] + series[1][self.label_column].unique()) - 1
    
    def _process_time_window(self, y_true, algo, tw_id, alpha=None):
        algo.computeMetrics()

    def _show_reports(self, *algos):
        print('+ Current Errors +')
        for algo in algos:
            algo.current_reportprint('AllPositive')
        print()
