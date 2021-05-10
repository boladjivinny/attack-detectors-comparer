from . import Algorithm

class TimeBasedAlgorithm(Algorithm):
    def __init__(self, name, X, y, labels, label_column='Label'):
        super().__init__(name, X, y, labels, label_column)

        # These are the values for the current time window only!
        self.cTP = 0 # a
        self.cTN = 0 # d
        self.cFP = 0 # c
        self.cFN = 0 # b
        self.cTPR = -1
        self.cTNR = -1
        self.cFNR = -1
        self.cFPR = -1
        self.cAccuracy = -1
        self.cPrecision = -1
        self.cErrorRate = -1
        self.cfmeasure1 = -1
        self.cfmeasure2 = -1
        self.cfmeasure05 = -1

    def current_reportprint(self, longest_name, precision=2):
        """ The reported values """ 
        # I still did not found out how to use longest_name to change the width of the columns...
        max_len = len(longest_name) + 1
        print (f'{self.name:{max_len}} TP={self.cTP}, TN={self.cTN}, '\
            f'FP={self.cFP}, FN={self.cFN}, TPR={self.cTPR:4.{precision}}, '\
            f'TNR={self.cTNR:.{precision}}, FPR={self.cFPR:.{precision}}, '\
            f'FNR={self.cFNR:.{precision}}, '\
            f'Precision={self.cPrecision:.{precision}}, '\
            f'Accuracy={self.cAccuracy:.{precision}}, '\
            f'ErrorRate={self.cErrorRate:.{precision}}, '\
            f'FM1={self.cfmeasure1:.{precision}}, '\
            f'FM2={self.cfmeasure2:.{precision}}, '\
            f'FM05={self.cfmeasure05:.{precision}}')

    def computeMetrics(self):
        """ Compute the metrics """ 
        try:
            assert (self.TP + self.FN) != 0
            self.TPR = self.TP / float( self.TP + self.FN )
            self.FNR = 1.0 - self.TPR
        except AssertionError:
            self.TPR = -1
            self.FNR = -1

        try:
            assert ( self.TN + self.FP ) != 0
            self.TNR = self.TN  / float( self.TN + self.FP )
            self.FPR = 1 - self.TNR
        except AssertionError:
            self.TNR = -1
            self.FPR = -1

        try:
            self.Precision = float(self.TP) / float( self.TP + self.FP)
        except ZeroDivisionError:
            self.Precision = -1

        try:
            assert ( self.TP + self.TN + self.FP + self.FN ) != 0
            self.Accuracy = ( self.TP + self.TN ) / float( self.TP + self.TN + self.FP + self.FN )
            self.ErrorRate = ( self.FN + self.FP ) / float( self.TP + self.TN + self.FP + self.FN )
        except AssertionError:
            self.Accuracy = -1
            self.ErrorRate = -1

        # F1-Measure.
        self.beta = 1.0
        # With beta=1 F-Measure is also Fscore
        try:
            self.fmeasure1 = ( ( (self.beta * self.beta) + 1 ) * self.Precision * self.TPR  ) / float( ( self.beta * self.beta * self.Precision ) + self.TPR )
        except ZeroDivisionError:
            self.fmeasure1 = -1

        # F2-Measure.
        self.beta = 2
        # With beta=2 F-Measure gives more importance to TPR (recall)
        try:
            self.fmeasure2 = ( ( (self.beta * self.beta) + 1 ) * self.Precision * self.TPR  ) / float( ( self.beta * self.beta * self.Precision ) + self.TPR )
        except ZeroDivisionError:
            self.fmeasure2 = -1

        # F0.5-Measure.
        self.beta = 0.5
        # With beta=2 F-Measure gives more importance to Precision
        try:
            self.fmeasure05 = ( ( (self.beta * self.beta) + 1 ) * self.Precision * self.TPR  ) / float( ( self.beta * self.beta * self.Precision ) + self.TPR )
        except ZeroDivisionError:
            self.fmeasure05 = -1

    @property
    def cTP(self):
        return self._cTP

    @cTP.setter
    def cTP(self, val):
        self._cTP = val
        self.TP += self._cTP

    @property
    def cTN(self):
        return self._cTN

    @cTN.setter
    def cTN(self, val):
        self._cTN = val
        self.TN += self._cTN

    @property
    def cFP(self):
        return self._cFP

    @cFP.setter
    def cFP(self, val):
        self._cFP = val
        self.FP += self._cFP

    @property
    def cFN(self):
        return self._cFN

    @cFN.setter
    def cFN(self, val):
        self._cFN = val
        self.FN += self._cFN
        