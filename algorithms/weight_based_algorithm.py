from numpy import iterable
from .time_based_algorithm import TimeBasedAlgorithm
import pandas as pd

class WeightBasedAlgorithm(TimeBasedAlgorithm):
    """Represents a detection technique compared using class weights.

    This class performs its comparison using weights for computing the
    metrics at each time window. 
    """
    def __init__(
        self, name: str, X: pd.DataFrame, y: list, 
        labels: list, label_column='Label'
    ):
        super().__init__(name, X, y, labels, label_column)

        # These are the cumulative weighted values
        self.t_TP = 0.0 # a
        self.t_TN = 0.0 # d
        self.t_FP = 0.0 # c
        self.t_FN = 0.0 # b
        self.t_TPR = -1.0
        self.t_TNR = -1.0
        self.t_FNR = -1.0
        self.t_FPR = -1.0
        self.t_Accuracy = -1.0
        self.t_Precision = -1.0
        self.t_ErrorRate = -1.0
        self.t_fmeasure1 = -1.0
        self.t_fmeasure2 = -1.0
        self.t_fmeasure05 = -1.0

        # These are the weighted values for the current time window only!
        self.ct_TP = 0.0 # a
        self.ct_TN = 0.0 # d
        self.ct_FP = 0.0 # c
        self.ct_FN = 0.0 # b
        self.ct_TPR = -1.0
        self.ct_TNR = -1.0
        self.ct_FNR = -1.0
        self.ct_FPR = -1.0
        self.ct_Accuracy = -1.0
        self.ct_Precision = -1.0
        self.ct_ErrorRate = -1.0
        self.ct_fmeasure1 = -1.0
        self.ct_fmeasure2 = -1.0
        self.ct_fmeasure05 = -1.0

    def logMetrics(self):
        self.rTPR += [self.t_TPR]
        self.rTNR += [self.t_TNR]
        self.rFPR += [self.t_FPR]
        self.rFNR += [self.t_FNR]
        self.rPrecision += [self.t_Precision]
        self.rAccuracy += [self.t_Accuracy]
        self.rErrorRate += [self.t_ErrorRate]
        self.rFM1 += [self.t_fmeasure1]
        self.rFM2 += [self.t_fmeasure2]
        self.rFM05 += [self.t_fmeasure05]

    def weighted_reportprint(self, max_name_length: int) -> None:
        """Prints the weighted metrics of the technique..

        This function prints out the weighted metrics evaluated for the 
        detection technique.

        Args:
            max_name_length (`int`): represents the total number of columns
                taken by the technique's name in the output.

        Returns:
            None
        """
        print (
            f'{self.name:{max_name_length}} TP={self.t_TP:8}, TN='\
            f'{self.t_TN:8}, FP={self.t_FP:8}, FN={self.t_FN:8}, TPR='\
            f'{self.t_TPR:.3f}, TNR={self.t_TNR:.3f}, FPR='\
            f'{self.t_FPR:.3f}'\
            f', FNR={self.t_FNR:.3f}, Precision={self.t_Precision:7.4f}, '\
            f'Accuracy={self.t_Accuracy:5.4f}, ErrorRate='\
            f'{self.t_ErrorRate:5.3f}, FM1={self.t_fmeasure1:7.4f}, '\
            f'FM2={self.t_fmeasure2:7.4f}, FM05={self.t_fmeasure05:7.4f}'
        )

    def weighted_current_reportprint(self, max_name_length: int):
        """Prints the weighted metrics for the current time window.

        This function prints out the weighted metrics evaluated for the 
        running time window in a human-readable format.

        Args:
            max_name_length (`int`): represents the total number of columns
                taken by the technique's name in the output.

        Returns:
            None
        """
        print (
            f'{self.name:{max_name_length}} TP={self.ct_TP:8}, TN='\
            f'{self.ct_TN:8}, FP={self.ct_FP:8}, FN={self.ct_FN:8}, TPR='\
            f'{self.ct_TPR:.3f}, TNR={self.ct_TNR:.3f}, FPR='\
            f'{self.ct_FPR:.3f}'\
            f', FNR={self.ct_FNR:.3f}, Precision={self.ct_Precision:7.4f}, '\
            f'Accuracy={self.ct_Accuracy:5.4f}, ErrorRate='\
            f'{self.ct_ErrorRate:5.3f}, FM1={self.ct_fmeasure1:7.4f}, '\
            f'FM2={self.ct_fmeasure2:7.4f}, FM05={self.ct_fmeasure05:7.4f}'
        )

    def csv_reportprint(self):
        return f'{self.name},{self.t_TP},{self.t_TN},{self.t_FP},{self.t_FN}'\
            f'{self.t_TPR},{self.t_TNR},{self.t_FPR},{self.t_FNR},'\
            f'{self.t_Precision},{self.t_Accuracy},{self.t_ErrorRate},'\
            f'{self.t_fmeasure1},{self.t_fmeasure2},{self.t_fmeasure05}'

    def compute_weighted_metrics(
        self, correcting_function: float, y_true: list
        ) -> None:
        """Compute the weighted metrics for the technique. 
        
        This method computes the weighted metrics based on the value of
        the correcting function passed.
        
        Args:
            correcting_function (`float`): the computed correction function.
            y_true (`list` or array-like): the true labels.

        Returns:
            None
        """ 
        pos_count = y_true.count(self.labels[1])
        neg_count = y_true.count(self.labels[0])

        if (pos_count != 0):
            self.ct_TP = (self.cTP * correcting_function) / float(pos_count)
            self.t_TP = self.t_TP + self.ct_TP
            self.ct_FN = (self.cFN * correcting_function) / float(pos_count)
            self.t_FN = self.t_FN + self.ct_FN
        
        if (neg_count !=0):
            self.ct_FP = self.cFP / float(neg_count)
            self.t_FP = self.t_FP + self.ct_FP
            self.ct_TN = self.cTN / float(neg_count)
            self.t_TN = self.t_TN + self.ct_TN

        try:
            self.t_TPR = self.t_TP / float(self.t_TP + self.t_FN)
        except ZeroDivisionError:
            self.t_TPR = -1
        try:
            self.ct_TPR = self.ct_TP / float(self.ct_TP + self.ct_FN)
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equivalent to do 
            # nothing.
            pass

        # t_TNR. Also Correct-reject rate or specificity. Portion of negative
        #  examples the model predicts correctly.
        try:
            self.t_TNR = self.t_TN / float( self.t_TN + self.t_FP )
        except ZeroDivisionError:
            self.t_TNR = -1
        try:
            self.ct_TNR = self.ct_TN / float( self.ct_TN + self.ct_FP )
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equivalent to do nothing.
            pass

        # t_FPR. Also False-alarm rate. The portion of negative examples that
        #  the model wrongly predicts as positive.
        try:
            self.t_FPR = self.t_FP / float( self.t_TN + self.t_FP )
        except ZeroDivisionError:
            self.t_FPR = -1
        try:
            self.ct_FPR = self.ct_FP / float( self.ct_TN + self.ct_FP )
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equivalent to do 
            # nothing.
            pass

        # t_FNR. Also Miss rate. Portion of positives examples that 
        # the classifier wrongly predicts as negative.
        try:
            self.t_FNR = self.t_FN / float(self.t_TP + self.t_FN)
        except ZeroDivisionError:
            self.t_FNR = -1
        try:
            self.ct_FNR = self.ct_FN / float(self.ct_TP + self.ct_FN)
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equivalent to do 
            # nothing.
            pass

        # t_Precision. Portion of all the examples predicted as positives 
        # that were really positives.
        try:
            self.t_Precision = float(self.t_TP) / float(
                self.t_TP + self.t_FP)
        except ZeroDivisionError:
            self.t_Precision = -1
        try:
            self.ct_Precision = float(self.ct_TP) / float(
                self.ct_TP + self.ct_FP)
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equivalent to do 
            # nothing.
            pass

        # t_Accuracy. The portion of examples that the model predicts 
        # correctly
        try:
            self.t_Accuracy = (self.t_TP + self.t_TN) / float(
                self.t_TP + self.t_TN + self.t_FP + self.t_FN )
        except ZeroDivisionError:
            self.t_Accuracy = -1
        try:
            self.ct_Accuracy = (self.ct_TP + self.ct_TN) / float(
                self.ct_TP + self.ct_TN + self.ct_FP + self.ct_FN)
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equivalent to do 
            # nothing.
            pass

        # t_Error Rate. The portion of examples that the model predicts 
        # incorrectly
        try:
            self.t_ErrorRate = (self.t_FN + self.t_FP) / float(
                self.t_TP + self.t_TN + self.t_FP + self.t_FN )
        except ZeroDivisionError:
            self.t_ErrorRate = -1
        try:
            self.ct_ErrorRate = (self.ct_FN + self.ct_FP) / float(
                self.ct_TP + self.ct_TN + self.ct_FP + self.ct_FN )
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equivalent to do 
            # nothing.
            pass

        t_fmeasure = lambda b, p, t: (
             ( (b * b) + 1 ) * p * t ) / float( ( b * b * p ) + t)
        # T1-Measure.
        beta = 1.0
        # With beta=1 F-Measure is also Fscore
        try:
            self.t_fmeasure1 = t_fmeasure(
                beta, self.t_Precision, self.t_TPR
            )
        except ZeroDivisionError:
            self.t_fmeasure1 = -1
        try:
            self.ct_fmeasure1 = t_fmeasure(
                beta, self.ct_Precision, self.ct_TPR
            )
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equivalent to do 
            # nothing.
            pass

        # T2-Measure.
        beta = 2.0
        # With beta=2 F-Measure gives more importance to TPR (recall)
        try:
            self.t_fmeasure2 = t_fmeasure(
                beta, self.t_Precision, self.t_TPR
            )
        except ZeroDivisionError:
            self.t_fmeasure2 = -1
        try:
            self.ct_fmeasure2 = t_fmeasure(
                beta, self.ct_Precision, self.ct_TPR
            )
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equivalent to do 
            # nothing.
            pass

        # F0.5-Measure.
        beta = 0.5
        # With beta=2 F-Measure gives more importance to Precision 
        try:
            self.t_fmeasure05 = t_fmeasure(
                beta, self.t_Precision, self.t_TPR
            )
        except ZeroDivisionError:
            self.t_fmeasure05 = -1
        try:
            self.ct_fmeasure05 = t_fmeasure(
                beta, self.ct_Precision, self.ct_TPR
            )
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equivalent to do 
            # nothing.
            pass