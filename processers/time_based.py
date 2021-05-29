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

        s = time.time()
        label_dict = {k: i for i, k in enumerate(self.labels)}

        for algo in args:
            data[algo.name] = [label_dict[x] for x in algo.data[self.label_column]]

        e = time.time()
        print(f'Processing done in {e - s} seconds.')
        window = 0
        remaining = data.shape[0]

        # initialize the start time
        start_time = data['StartTime'].min()

        while (remaining > 0):
            s = time.time()
            end_time = start_time + datetime.timedelta(seconds=window_size)
            chunk = data.loc[(data['StartTime'] >= start_time) & (data['StartTime'] < end_time)]
            start_time = data.loc[data['StartTime'] >= end_time, 'StartTime'].min()
            remaining -= len(chunk)
            window += 1
            true_y = None
            e = time.time()
            print(f'Time window {window}')
            print(f'Retrieved the data in {e - s} seconds.')
            # now the labels for each algorithm and we compared
            s = time.time()
            grouped = chunk.groupby('SrcAddr')
            #ips = [k for k, _ in grouped]
            e = time.time()
            print(f'Retrieved list of ips in {e - s} seconds.')
            s = time.time()
            #label_dict = {k: i for i, k in enumerate(self.labels)}
            # for each series, convert to the index and take the max
            # technique_labels = [
            #     [
            #         *map(lambda s: s[1][algo.name].apply(lambda d: label_dict[d]).max(), grouped)
            #     ]
            #     for algo in args
            # ]
            # technique_labels = [
            #     [max(d[1].to_list()) for d in grouped[algo.name]]
            #     for algo in args
            # ]

            technique_labels = map(lambda algo: [*map(lambda d: max(d[1].to_list()), grouped[algo.name])], args)
            
            #[[*map(lambda s: s[1][algo.name].max(), grouped)] for algo in args]
            #technique_labels = list(map(lambda algo: list(map(lambda s: int(self.labels[1] in s[1][algo.name].tolist()), grouped)), args))
            e = time.time()
            print(f'Retrieved all the labels in {e - s} seconds.')

            ss = time.time()
            for algo, y in zip(args, technique_labels):
                #y = [d[0] for d in y]
                # print(y)
                if true_y is None:
                    # reference is expected to be the first one
                    true_y = y
                    true_labels = list(map(lambda x: self.labels[x], true_y))

                    if verbose > 0:
                        print("####################################")
                        print(f'Time Window Number: {window}')
                        print(f'Amount of algorithms being used: {len(args)-1}')
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
                    for (addr, _), ty, py in zip(grouped, true_y, y):
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
                e = time.time()
                print(f'Collected the basic metrics in {e - s} seconds.')
                s = time.time()
                self._process_time_window(true_labels, algo, window, alpha)
                e = time.time()
                print(f'Process all the computations in {e - s} seconds.')
            
            ee = time.time()
            print(f"Processing for all algos took {ee - ss} seconds")
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
