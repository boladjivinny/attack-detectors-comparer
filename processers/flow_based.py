from .base import BaseProcesser
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score
from sklearn.metrics import f1_score, fbeta_score

class FlowBasedProcesser(BaseProcesser):
    # the arguments should be the techniques
    def __init__(self, label_column, labels):
        self.label_column = label_column
        self.labels = labels


    def __call__(self, reference, *args, window_size=None, alpha=None, verbose=0):
        # here we need to compare the results
        true_y = reference.data[self.label_column]

        for algo in args:
            y = algo.data[self.label_column]
            algo.TN, algo.FP, algo.FN, algo.TP = confusion_matrix(
                true_y, y, labels=self.labels[:3]).ravel()
            algo.TNR, algo.FPR, algo.FNR, algo.TPR = confusion_matrix(
                true_y, y, normalize='all', labels=self.labels[:3]).ravel()
            algo.Accuracy = accuracy_score(true_y, y, normalize=True)
            algo.Precision = precision_score(true_y, y, 
                labels=self.labels[:3], pos_label=self.labels[1])
            algo.fmeasure1 = f1_score(true_y, y, 
                labels=self.labels[:3], pos_label=self.labels[1])
            algo.fmeasure2 = fbeta_score(true_y, y, beta=2, 
                labels=self.labels[:3], pos_label=self.labels[1])
            algo.fmeasure05 = fbeta_score(true_y, y, beta=0.5, 
                labels=self.labels[:3], pos_label=self.labels[1])
            try:
                algo.ErrorRate = (algo.FN + algo.FP) / (algo.TN 
                    + algo.FP + algo.FN + algo.TP)
            except ZeroDivisionError:
                algo.ErrorRate = -1