from datetime import datetime

class Algorithm:
    # X is just starttime, and the source IP address
    def __init__(self, name, X, y, labels, label_column='Label'):
        assert X.shape[0] == y.shape[0]

        self.name = name
        self.label = label_column
        self.labels = labels
        self._data = X
        self._data[self.label] = y

        # the metrics
        self.TP = 0 # a
        self.TN = 0 # d
        self.FP = 0 # c
        self.FN = 0 # b
        self.B1 = 0 # Predicted negative and real was background
        self.B2 = 0 # Predicted positive and real was background
        self.B3 = 0 # Predicted background and real was negative
        self.B4 = 0 # Predicted background and real was positive
        self.B5 = 0 # Predicted background and real was background
        self.TPR = -1
        self.TNR = -1
        self.FNR = -1
        self.FPR = -1
        self.Accuracy = -1
        self.Precision = -1
        self.ErrorRate = -1
        self.fmeasure1 = -1
        self.fmeasure2 = -1
        self.fmeasure05 = -1


    def __call__(self, date: datetime, srcIP: str):
        return self._data.loc[
            self._data.StartTime == date & self._data.SrcAddr == srcIP,
             self.label]

    def __repr__(self):
        """ Default printing method """ 
        return f'{self.name} TP={self.TP}, TN={self.TN}, FP={self.FP}, '\
            f'FN={self.FN} TPR={self.TPR:.2f}, TNR={self.TNR:.2f}, '\
            f'FPR={self.FPR:.2f}, FNR={self.FNR:.2f}, '\
            f'Precision={self.Precision:.2f}, Accuracy={self.Accuracy:.2f}, '\
            f'ErrorRate={self.ErrorRate:.2f}, FM1={self.fmeasure1:.2f}, '\
            f'FM2={self.fmeasure2:.2f}, FM05={self.fmeasure05:.2f}'


    @property
    def data(self):
        return self._data