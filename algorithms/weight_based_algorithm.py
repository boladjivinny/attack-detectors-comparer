from .time_based_algorithm import TimeBasedAlgorithm

class WeightBasedAlgorithm(TimeBasedAlgorithm):
    def __init__(self, name, X, y, labels, label_column='Label'):
        super().__init__(name, X, y, labels, label_column)

        # These are the cumulative weighted values
        self.t_TP = 0.0 # a
        self.t_TN = 0.0 # d
        self.t_FP = 0.0 # c
        self.t_FN = 0.0 # b
        self.t_B1 = 0.0 # Predicted negative and real was background
        self.t_B2 = 0.0 # Predicted positive and real was background
        self.t_B3 = 0.0 # Predicted background and real was negative
        self.t_B4 = 0.0 # Predicted background and real was positive
        self.t_B5 = 0.0 # Predicted background and real was background
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

    def weighted_reportprint(self, longest_name):
        """ The reported values """ 
        # I still did not found out how to use longest_name to change the width of the columns...
        text = '{0:30} t-TP={1:.4f}, t-TN={2:8}, t-FP={3:8}, t-FN={4:.4f}, t-TPR={5:.3f}, t-TNR={6:.3f}, t-FPR={7:.3f}, t-FNR={8:.3f}, t-Precision={9:7.4f}, t-Accuracy={10:5.4f}, t-ErrorRate={11:5.3f}, t-FM1={12:7.4f}, t-FM2={13:7.4f}, t-FM05={14:7.4f}, t-B1={15:8}, t-B2={16:8}, t-B3={17:3}, t-B4={18:3}, t-B5={19:3}'.format(self.name, self.t_TP, self.t_TN, self.t_FP, self.t_FN, self.t_TPR, self.t_TNR, self.t_FPR, self.t_FNR, self.t_Precision, self.t_Accuracy, self.t_ErrorRate, self.t_fmeasure1, self.t_fmeasure2, self.t_fmeasure05, self.t_B1, self.t_B2, self.t_B3, self.t_B4, self.t_B5)
        print (text)

    def weighted_current_reportprint(self, longest_name):
        """ The reported values """ 
        # I still did not found out how to use longest_name to change the width of the columns...
        print ('{0:30} t-TP={1:.4f}, t-TN={2:8}, t-FP={3:8}, t-FN={4:.4f}, t-TPR={5:.3f}, t-TNR={6:.3f}, t-FPR={7:.3f}, t-FNR={8:.3f}, t-Precision={9:7.4f}, t-Accuracy={10:5.4f}, t-ErrorRate={11:5.3f}, t-FM1={12:7.4f}, t-FM2={13:7.4f}, t-FM05={14:7.4f}, t-B1={15:8}, t-B2={16:8}, t-B3={17:3}, t-B4={18:3}, t-B5={19:3}'.format(self.name, self.ct_TP, self.ct_TN, self.ct_FP, self.ct_FN, self.ct_TPR, self.ct_TNR, self.ct_FPR, self.ct_FNR, self.ct_Precision, self.ct_Accuracy, self.ct_ErrorRate, self.ct_fmeasure1, self.ct_fmeasure2, self.ct_fmeasure05, self.ct_B1, self.ct_B2, self.ct_B3, self.ct_B4, self.ct_B5))


    def compute_weighted_metrics(self, correcting_function, y_true):
        """ Compute the weighted metrics. Receives the correcting_function value and the amount of labels in the current time window """ 
        pos_count = y_true.count(self.labels[1])
        neg_count = y_true.count(self.labels[0])

        if (pos_count != 0):
            self.ct_TP = ( self.cTP * correcting_function ) / float(pos_count)
            self.t_TP = self.t_TP + self.ct_TP
            self.ct_FN = ( self.cFN * correcting_function ) / float(pos_count)
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
            # We should add 0 to the current value, that is equal to do nothing.
            pass

        # t_TNR. Also Correct-reject rate or specificity. Portion of negative examples the model predicts correctly.
        try:
            self.t_TNR = self.t_TN / float( self.t_TN + self.t_FP )
        except ZeroDivisionError:
            self.t_TNR = -1
        try:
            self.ct_TNR = self.ct_TN / float( self.ct_TN + self.ct_FP )
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equal to do nothing.
            pass

        # t_FPR. Also False-alarm rate. The portion of negative examples that the model wrongly predicts as positive.
        try:
            self.t_FPR = self.t_FP / float( self.t_TN + self.t_FP )
        except ZeroDivisionError:
            self.t_FPR = -1
        try:
            self.ct_FPR = self.ct_FP / float( self.ct_TN + self.ct_FP )
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equal to do nothing.
            pass

        # t_FNR. Also Miss rate. Portion of positives examples that the classifier wrongly predicts as negative.
        try:
            self.t_FNR = self.t_FN / float(self.t_TP + self.t_FN)
        except ZeroDivisionError:
            self.t_FNR = -1
        try:
            self.ct_FNR = self.ct_FN / float(self.ct_TP + self.ct_FN)
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equal to do nothing.
            pass

        # t_Precision. Portion of all the examples predicted as positives that were really positives.
        try:
            self.t_Precision = float(self.t_TP) / float(self.t_TP + self.t_FP)
        except ZeroDivisionError:
            self.t_Precision = -1
        try:
            self.ct_Precision = float(self.ct_TP) / float(self.ct_TP + self.ct_FP)
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equal to do nothing.
            pass

        # t_Accuracy. The portion of examples that the model predicts correctly
        try:
            self.t_Accuracy = (self.t_TP + self.t_TN) / float( self.t_TP + self.t_TN + self.t_FP + self.t_FN )
        except ZeroDivisionError:
            self.t_Accuracy = -1
        try:
            self.ct_Accuracy = (self.ct_TP + self.ct_TN) / float( self.ct_TP + self.ct_TN + self.ct_FP + self.ct_FN )
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equal to do nothing.
            pass

        # t_Error Rate. The portion of examples that the model predicts incorrectly
        try:
            self.t_ErrorRate = (self.t_FN + self.t_FP) / float( self.t_TP + self.t_TN + self.t_FP + self.t_FN )
        except ZeroDivisionError:
            self.t_ErrorRate = -1
        try:
            self.ct_ErrorRate = (self.ct_FN + self.ct_FP) / float( self.ct_TP + self.ct_TN + self.ct_FP + self.ct_FN )
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equal to do nothing.
            pass

        # T1-Measure.
        self.beta = 1.0
        # With beta=1 F-Measure is also Fscore
        try:
            self.t_fmeasure1 = ( ( (self.beta * self.beta) + 1 ) * self.t_Precision * self.t_TPR  ) / float( ( self.beta * self.beta * self.t_Precision ) + self.t_TPR )
        except ZeroDivisionError:
            self.t_fmeasure1 = -1
        try:
            self.ct_fmeasure1 = ( ( (self.beta * self.beta) + 1 ) * self.ct_Precision * self.ct_TPR  ) / float( ( self.beta * self.beta * self.ct_Precision ) + self.ct_TPR )
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equal to do nothing.
            pass

        # T2-Measure.
        self.beta = 2.0
        # With beta=2 F-Measure gives more importance to TPR (recall)
        try:
            self.t_fmeasure2 = ( ( (self.beta * self.beta) + 1 ) * self.t_Precision * self.t_TPR  ) / float( ( self.beta * self.beta * self.t_Precision ) + self.t_TPR )
        except ZeroDivisionError:
            self.t_fmeasure2 = -1
        try:
            self.ct_fmeasure2 = ( ( (self.beta * self.beta) + 1 ) * self.ct_Precision * self.ct_TPR  ) / float( ( self.beta * self.beta * self.ct_Precision ) + self.ct_TPR )
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equal to do nothing.
            pass

        # F0.5-Measure.
        self.beta = 0.5
        # With beta=2 F-Measure gives more importance to Precision 
        try:
            self.t_fmeasure05 = ( ( (self.beta * self.beta) + 1 ) * self.t_Precision * self.t_TPR  ) / float( ( self.beta * self.beta * self.t_Precision ) + self.t_TPR )
        except ZeroDivisionError:
            self.t_fmeasure05 = -1
        try:
            self.ct_fmeasure05 = ( ( (self.beta * self.beta) + 1 ) * self.ct_Precision * self.ct_TPR  ) / float( ( self.beta * self.beta * self.ct_Precision ) + self.ct_TPR )
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equal to do nothing.
            pass


    def __repr__(self):
        return repr(f'{self.name} t-TP={self.t_TP:.2f}, t-TN={self.t_TN:.2f},'\
            f' t-FP={self.t_FP:.2f}, t-FN={self.t_FN:.2f}, '\
            f't-TPR={self.t_TPR:.2f}, t-TNR={self.t_TNR:.2f}, '\
            f't-FPR={self.t_FPR:.2f}, t-FNR={self.t_FNR:.2f}, '\
            f't-Precision={self.t_Precision:.2f}, t-Accuracy='\
            f'{self.t_Accuracy:.2f}, t-ErrorRate={self.t_ErrorRate:.2f}, '\
            f't-FM1={self.t_fmeasure1:.2f}, t-FM2={self.t_fmeasure2:.2f}, '\
            f't-FM05={self.t_fmeasure05:.2f}')