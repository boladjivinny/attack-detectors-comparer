import pandas as pd
import datetime
import time

from .base import BaseProcesser
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score
from sklearn.metrics import f1_score, fbeta_score

class TimeBasedProcesser(BaseProcesser):
    # the arguments should be the techniques
    def __init__(self, label_column, labels):
        self.label_column = label_column
        self.labels = labels

    def __call__(self, window_size, reference, *args, **kwargs):
        # here we need to compare the results

        #true_y = reference.data[self.label_column]
        data = reference.data.copy()
        data['Timeframe'] = -1
        cur = 1
        #print(data['Timeframe'].tolist())

        start = time.time()
        while (data.loc[data.Timeframe == -1].shape[0] > 0):
            #print("in there")
            # find the min
            start_time = data.loc[data.Timeframe == -1, 'StartTime'].min()
            data.loc[(data.StartTime >= start_time) & (data.StartTime < start_time + datetime.timedelta(seconds=window_size)), 'Timeframe'] = cur
            cur += 1
        end = time.time()
        #start_time = data['StartTime'].min()
        # data['Timeframe'] = (((
        #     data['StartTime'] - start_time).dt.total_seconds(
        #         ).astype('int')) // time) + 1

        # print(data['Timeframe'].unique())
        # print(data['Timeframe'].nunique())

        # exit()

        # 
        #print(reference.data.groupby('Timeframe').head())
        for window, chunk in data.groupby('Timeframe'):
            # here we collect the statistics time based ones and 
            # make sure they are cumulated
            # collect the true labels according to the authors' strategy
            # assign the normal label by default


            ips_to_labels = {
                ip: self.labels[1] if self.labels[1] in records[
                    self.label_column].unique() 
                    else self.labels[0] for ip, records in chunk.groupby(
                        'SrcAddr')}
            true_y = [v for k, v in ips_to_labels.items()]

            print("####################################")
            print(f'Time Window Number: {window}')
            print(f'Amount of algorithms being used: {len(args)}')
            ips_report = {ll: true_y.count(ll) for ll in self.labels}
            print(f'Amount of unique ips: {ips_report}')
            labels_report = dict(chunk.Label.value_counts())
            print(f'Amount of labels: {labels_report}')
            print(f'Lines read: {chunk.shape[0]}')
            print('####################################')


            # now the labels for each algorithm and we compared
            for algo in args:
                seq = algo.data.loc[data.index, :]
                algo_labels = {
                ip: self.labels[1] if self.labels[1] in seq[
                    self.label_column].unique() 
                    else self.labels[0] for ip, records in seq.groupby(
                        'SrcAddr')}
                print("collected results")
                y = [algo_labels[ip] for ip in ips_to_labels.keys()]
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

                print("starting the process")

                self._process_time_window(true_y, algo, window, **kwargs)
                print("done")
            
            self._show_reports(algos)

        # # generare the time windows
        # # print the final report
        # for algo in args:
        #     algo.computeMetrics()

    def _process_time_window(self, y_true, algo, tw_id, **kwargs):
        algo.computeMetrics()

    def _show_reports(self, algos):
        print('+ Current Errors +')
        for algo in algos:
            algo.current_reportprint()