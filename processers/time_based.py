import datetime

from .base import BaseProcesser
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score
from sklearn.metrics import f1_score, fbeta_score

class TimeBasedProcesser(BaseProcesser):
    # the arguments should be the techniques
    def __init__(self, label_column, labels):
        self.label_column = label_column
        self.labels = labels

    def __call__(self, reference, *args, window_size=None, alpha=None, verbose=0):
        data = reference.data
        data['Timeframe'] = -1
        cur = 1
        #print(data['Timeframe'].tolist())

        while (data.loc[data.Timeframe == -1].shape[0] > 0):
            #print("in there")
            # find the min
            start_time = data.loc[data.Timeframe == -1, 'StartTime'].min()
            data.loc[(data.StartTime >= start_time) & (data.StartTime < start_time + datetime.timedelta(seconds=window_size)), 'Timeframe'] = cur
            cur += 1

        for window, chunk in data.groupby('Timeframe'):
            ips_to_labels = {
                ip: self.labels[1] if self.labels[1] in records[
                    self.label_column].unique() 
                    else self.labels[0] for ip, records in chunk.groupby(
                        'SrcAddr')}
            
            true_y = [v for _, v in ips_to_labels.items()]

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
            for algo in args:
                seq = algo.data.loc[chunk.index, :]
                algo_labels = {
                ip: self.labels[1] if self.labels[1] in records[
                    self.label_column].unique() 
                    else self.labels[0] for ip, records in seq.groupby(
                        'SrcAddr')}
                y = [algo_labels[ip] for ip in ips_to_labels.keys()]

                # display errors
                if verbose > 1:
                    for addr, ty, py in zip(ips_to_labels.keys(), true_y, y):
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

                algo.cTN, algo.cFP, algo.cFN, algo.cTP = confusion_matrix(
                    true_y, y, labels=self.labels[:3]).ravel()
                algo.cTNR, algo.cFPR, algo.cFNR, algo.cTPR = confusion_matrix(
                    true_y, y, normalize='true', labels=self.labels[:3]
                    ).ravel()
                algo.cAccuracy = accuracy_score(true_y, y, normalize=True)
                algo.cPrecision = precision_score(true_y, y, 
                    labels=self.labels[:3], pos_label=self.labels[1], 
                    zero_division=0)
                algo.cfmeasure1 = f1_score(true_y, y, 
                    labels=self.labels[:3], pos_label=self.labels[1],
                    zero_division=0)
                algo.cfmeasure2 = fbeta_score(true_y, y, beta=2, 
                    labels=self.labels[:3], pos_label=self.labels[1],
                    zero_division=0)
                algo.cfmeasure05 = fbeta_score(true_y, y, beta=5, 
                    labels=self.labels[:3], pos_label=self.labels[1],
                    zero_division=0)
                try:
                    algo.cErrorRate = (algo.FN + algo.FP) / (algo.TN 
                        + algo.FP + algo.FN + algo.TP)
                except ZeroDivisionError:
                    algo.cErrorRate = -1
                self._process_time_window(true_y, algo, window, alpha)
            
            if verbose > 0:
                self._show_reports(*args)

    def _process_time_window(self, y_true, algo, tw_id, alpha=None):
        algo.computeMetrics()

    def _show_reports(self, *algos):
        print('+ Current Errors +')
        for algo in algos:
            algo.current_reportprint('AllPositive')
        print()
