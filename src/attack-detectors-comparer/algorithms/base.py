import pandas as pd

class Algorithm:
    """Represents the base class for the detection techniques.

    This default class performs a flow-by-flow comparison
    and output its metrics based on the same.

    Attributes:
        name (`str`): the name of the detection technique.
        label (`str`): the name of the column representing the 
            technique's prediction.
        labels (`list`): the two labels to be expected in the predictions.
        data (`pandas.DataFrame`): the features plus the output of the
            technique.
    """
    # X is just starttime, and the source IP address
    def __init__(
        self, name: str, X: pd.DataFrame, y: list, 
        labels: list, label_column='Label'
    ):
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

        return self


    def computeMetrics(self):
        """Compute the metrics for the detection technique.

        Given the count of True Positive, False Positive,
        True Negative and False Negative encountered, this method computes
        the relevant statistics for the detection technique.

        Args:
            None

        Returns:
            self: the object representing the detection technique
        """ 
        try:
            self.TPR = float(self.TP) / float(self.TP + self.FN)
            self.FNR = 1.0 - self.TPR
        except ZeroDivisionError:
            self.TPR = -1.0
            self.FNR = -1.0

        try:
            self.TNR = float(self.TN) / float(self.TN + self.FP)
            self.FPR = 1 - self.TNR
        except ZeroDivisionError:
            self.TNR = -1.0
            self.FPR = -1.0

        try:
            self.Precision = float(self.TP) / float(self.TP + self.FP)
        except ZeroDivisionError:
            self.Precision = -1.0

        try:
            self.Accuracy = ( self.TP + self.TN ) / float( 
                self.TP + self.TN + self.FP + self.FN )
        except ZeroDivisionError:
            self.Accuracy = -1.0

        try:
            self.ErrorRate = ( self.FN + self.FP ) / float( 
                self.TP + self.TN + self.FP + self.FN )
        except AssertionError:
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

        return self

    def f_score(self, beta=1.0) -> float:
        """Compute the F-Measure metric for the technique.

        Evaluates the F-measure metric for the detection technique, given the
        beta value.

        Args:
            beta (`float`): the value of beta to use for the computation.

        Returns:
            `float`: the result of the computation.
        """
        return ( 
            ( (beta * beta) + 1 ) * self.Precision * self.TPR  ) / float(
             ( beta * beta * self.Precision ) + self.TPR )


    def reportprint(self, max_name_length: int) -> None:
        """Prints the detailed statistical metrics for the technique.

        This method prints out the estimation of the metrics for the 
        detection technique in a human-readable format. 

        Args:
            max_name_length (`int`): represents the total number of columns
                taken by the technique's name in the output.

        Returns:
            None
        """ 
        print (
            f'{self.name:{max_name_length}} TP={self.TP:8}, TN={self.TN:8},'\
            f'FP={self.FP:8}, FN={self.FN:8}, TPR={self.TPR:.3f}, '\
            f'TNR={self.TNR:.3f}, FPR={self.FPR:.3f}, FNR={self.FNR:.3f}, '\
            f'Precision={self.Precision:7.4f}, Accuracy={self.Accuracy:5.4f}'\
            f', ErrorRate={self.ErrorRate:5.3f}, FM1={self.fmeasure1:7.4f}, '\
            f'FM2={self.fmeasure2:7.4f}, FM05={self.fmeasure05:7.4f}'
        )
    
    def csv_reportprint(self) -> str:
        """Returns a CSV representation of the metrics computed.

        This function prints out the metrics in a comma separated
        format to be saved in a file.

        Args:
            None

        Returns:
            the CSV representation of the metrics.
        """
        return f'{self.name},{self.TP},{self.TN},{self.FP},{self.FN},'\
            f'{self.TPR},{self.TNR},{self.FPR},{self.FNR},'\
            f'{self.Precision},{self.Accuracy},{self.ErrorRate},'\
            f'{self.fmeasure1},{self.fmeasure2},{self.fmeasure05}'

    def __str__(self) -> str:
        return self.name


    @property
    def data(self) -> pd.DataFrame:
        """Returns the data (features + label) of the technique.
        """
        return self._data
