import datetime
import time

from .base import BaseProcesser
from sklearn.metrics import confusion_matrix

class TimeBasedProcesser(BaseProcesser):
    # the arguments should be the techniques
    def __init__(self, label_column, labels):
        self.label_column = label_column
        self.labels = labels

    def __call__(self, reference, *args, window_size=None, alpha=None, verbose=0):
        data = reference.data
        data['Timeframe'] = -1

        for algo in args:
            data[algo.name] = algo.data[self.label_column]
        window = 0
        processed = 0

        while (processed < data.shape[0]):
            s = time.time()
            remainder = data.loc[data.Timeframe == -1]
            start_time = remainder['StartTime'].min()
            chunk = remainder.loc[(remainder.StartTime >= start_time) & (remainder.StartTime < start_time + datetime.timedelta(seconds=window_size))]
            data.loc[chunk.index, 'Timeframe'] = window
            processed += chunk.shape[0]
            window += 1
            data_by_ip = chunk.groupby('SrcAddr')
            e = time.time()

            print(f'collected the required information in {e - s} seconds.')

            s = time.time()
            true_y = [self.labels[1] if record[self.label_column].isin(self.labels[1:]).any() else self.labels[0] for _, record in data_by_ip]
            e = time.time()
            print(f'retrieved the true labels in  {e - s} seconds.')

            if verbose > 0:
                print("####################################")
                print(f'Time Window Number: {window}')
                print(f'Amount of algorithms being used: {len(args)}')
                ips_report = {ll: true_y.count(ll) for ll in self.labels}
                print(f'Amount of unique ips: {ips_report}')
                labels_report = dict(chunk[self.label_column].value_counts())
                print(f'Amount of labels: {labels_report}')
                print(f'Lines read: {chunk.shape[0]}')
                print('####################################')
                print()

            # now the labels for each algorithm and we compared
            ips = chunk.SrcAddr.unique()
            for algo in args:
                s = time.time()
                y = [self.labels[1] if record[algo.name].isin(self.labels[1:]).any() else self.labels[0] for _, record in data_by_ip]
                e = time.time()
                print(f'retrieved the labels for {algo.name} in  {e - s} seconds.')


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
                    true_y, y, labels=self.labels[:3]).ravel()
                self._process_time_window(true_y, algo, window, alpha)
                e = time.time()
                print(f'computed the metrics for {algo.name} in  {e - s} seconds.')
            
            if verbose > 0:
                self._show_reports(*args)


    def _process_time_window(self, y_true, algo, tw_id, alpha=None):
        algo.computeMetrics()

    def _show_reports(self, *algos):
        print('+ Current Errors +')
        for algo in algos:
            algo.current_reportprint('AllPositive')
        print()
