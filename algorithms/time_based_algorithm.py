from pandas.core.frame import DataFrame
from . import Algorithm

class TimeBasedAlgorithm(Algorithm):
    """Represents a detection technique compared using timeframes.

    This class extends the base class and add time based metrics
    intended at being used for timeframe to timeframe evaluation
    of the performances of the algorithms. This uses source IP
    addresses rather than flow entries for comparison.
    """
    def __init__(self, name: str, X: DataFrame, y: list, labels: list, label_column='Label'):
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

        # records of values across the timeframes
        self.rTPR = []
        self.rTNR = []
        self.rFPR = []
        self.rFNR = []
        self.rPrecision = []
        self.rAccuracy = []
        self.rErrorRate = []
        self.rFM1 = []
        self.rFM2 = []
        self.rFM05 = []

    def current_reportprint(self, max_name_length: int) -> None:
        """Prints the results of the current time window.

        This function prints out the metrics evaluated for the running
        time window in a human-readable format.

        Args:
            max_name_length (`int`): represents the total number of columns
                taken by the technique's name in the output.

        Returns:
            None
        """
        print (
            f'{self.name:{max_name_length}} TP={self.cTP:8}, TN='\
            f'{self.cTN:8}, FP={self.cFP:8}, FN={self.cFN:8}, TPR='\
            f'{self.cTPR:.3f}, TNR={self.cTNR:.3f}, FPR={self.cFPR:.3f}'\
            f', FNR={self.cFNR:.3f}, Precision={self.cPrecision:7.4f}, '\
            f'Accuracy={self.cAccuracy:5.4f}, ErrorRate='\
            f'{self.cErrorRate:5.3f}, FM1={self.cfmeasure1:7.4f}, '\
            f'FM2={self.cfmeasure2:7.4f}, FM05={self.cfmeasure05:7.4f}'
        )

    def logMetrics(self) -> None:
        """Records the values of the metrics for each time window.

        This function stores the values of the comparison metrics 
        for time window being processed at the invocation time.
        """
        self.rTPR += [self.TPR]
        self.rTNR += [self.TNR]
        self.rFPR += [self.FPR]
        self.rFNR += [self.FNR]
        self.rPrecision += [self.Precision]
        self.rAccuracy += [self.Accuracy]
        self.rErrorRate += [self.ErrorRate]
        self.rFM1 += [self.fmeasure1]
        self.rFM2 += [self.fmeasure2]
        self.rFM05 += [self.fmeasure05]

    def computeMetrics(self):
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


    # Getters and setters for the basic metrics.
    # When updating the current values, increase the cumulative metrics too.
    
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