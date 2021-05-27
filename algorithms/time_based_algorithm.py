from . import Algorithm

class TimeBasedAlgorithm(Algorithm):
    def __init__(self, name, X, y, labels, label_column='Label'):
        super().__init__(name, X, y, labels, label_column)

        # These are the values for the current time window only!
        self.cTP = 0 # a
        self.cTN = 0 # d
        self.cFP = 0 # c
        self.cFN = 0 # b
        self.cTPR = -1.0
        self.cTNR = -1.0
        self.cFNR = -1.0
        self.cFPR = -1.0
        self.cAccuracy = -1.0
        self.cPrecision = -1.0
        self.cErrorRate = -1.0
        self.cfmeasure1 = -1.0
        self.cfmeasure2 = -1.0
        self.cfmeasure05 = -1.0

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
        super().computeMetrics()
        try:
            self.cTPR = float(self.cTP) / float( self.cTP + self.cFN )
            self.cFNR = 1.0 - self.cTPR
        except ZeroDivisionError:
            self.cTPR = -1.0
            self.cFNR = -1.0

        try:
            self.cTNR = float(self.cTN)  / float( self.cTN + self.cFP )
            self.cFPR = 1 - self.cTNR
        except ZeroDivisionError:
            self.cTNR = -1.0
            self.cFPR = -1.0

        try:
            self.cPrecision = float(self.cTP) / float( self.cTP + self.cFP)
        except ZeroDivisionError:
            self.cPrecision = -1.0

        try:
            self.cAccuracy = ( self.cTP + self.cTN ) / float( self.cTP + self.cTN + self.cFP + self.cFN )
        except ZeroDivisionError:
            self.cAccuracy = -1.0

        try:
            self.cErrorRate = ( self.cFN + self.cFP ) / float( self.cTP + self.cTN + self.cFP + self.cFN )
        except AssertionError:
            self.cErrorRate = -1.0

        # F1-Measure.
        # With beta=1 F-Measure is also Fscore
        try:
            self.cfmeasure1 = self.f_score()
        except ZeroDivisionError:
            self.cfmeasure1 = -1.0

        # With beta=2 F-Measure gives more importance to TPR (recall)
        try:
            self.cfmeasure2 = self.f_score(2.0)
        except ZeroDivisionError:
            self.cfmeasure2 = -1.0

        # F0.5-Measure.
        # With beta=0.5 F-Measure gives more importance to Precision
        try:
            self.cfmeasure05 = self.f_score(0.5)
        except ZeroDivisionError:
            self.cfmeasure05 = -1.0

    def f_score(self, beta=1.0):
        return ( ( (beta * beta) + 1 ) * self.cPrecision * self.cTPR  ) / float( ( beta * beta * self.cPrecision ) + self.cTPR )


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
        