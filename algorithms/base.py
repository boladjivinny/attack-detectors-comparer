import pandas as pd

class Algorithm:
    # X is just starttime, and the source IP address
    def __init__(self, name, X, y, labels, label_column='Label'):
        if X is not None:
            assert X.shape[0] == len(y)

        self.name = name
        self.label = label_column
        self.labels = labels
        if X is not None:
            self._data = X.copy()
        else:
            self._data = pd.DataFrame()
        self._data[self.label] = y.copy()


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
        self.TPR = -1.0
        self.TNR = -1.0
        self.FNR = -1.0
        self.FPR = -1.0
        self.Accuracy = -1.0
        self.Precision = -1.0
        self.ErrorRate = -1.0
        self.fmeasure1 = -1.0
        self.fmeasure2 = -1.0
        self.fmeasure05 = -1.0

    def computeMetrics(self):
        """ Compute the metrics """ 
        try:
            assert (self.TP + self.FN) != 0
            self.TPR = self.TP / float( self.TP + self.FN )
            self.FNR = 1.0 - self.TPR
        except AssertionError:
            self.TPR = -1.0
            self.FNR = -1.0

        try:
            assert ( self.TN + self.FP ) != 0
            self.TNR = self.TN  / float( self.TN + self.FP )
            self.FPR = 1 - self.TNR
        except AssertionError:
            self.TNR = -1.0
            self.FPR = -1.0

        try:
            self.Precision = float(self.TP) / float( self.TP + self.FP)
        except ZeroDivisionError:
            self.Precision = -1.0

        try:
            assert ( self.TP + self.TN + self.FP + self.FN ) != 0
            self.Accuracy = ( self.TP + self.TN ) / float( self.TP + self.TN + self.FP + self.FN )
            self.ErrorRate = ( self.FN + self.FP ) / float( self.TP + self.TN + self.FP + self.FN )
        except AssertionError:
            self.Accuracy = -1.0
            self.ErrorRate = -1.0

        # F1-Measure.
        # With beta=1 F-Measure is also Fscore
        try:
            self.fmeasure1 = self.f_score()
        except ZeroDivisionError:
            self.fmeasure1 = -1.0

        # With beta=2 F-Measure gives more importance to TPR (recall)
        try:
            self.fmeasure2 = self.f_score(2.0)
        except ZeroDivisionError:
            self.fmeasure2 = -1.0

        # F0.5-Measure.
        # With beta=0.5 F-Measure gives more importance to Precision
        try:
            self.fmeasure05 = self.f_score(0.5)
        except ZeroDivisionError:
            self.fmeasure05 = -1.0

    def f_score(self, beta=1.0):
        return ( ( (beta * beta) + 1 ) * self.Precision * self.TPR  ) / float( ( beta * beta * self.Precision ) + self.TPR )


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
