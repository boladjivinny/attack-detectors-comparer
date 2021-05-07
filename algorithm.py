from . import *

class algorithm():
    """ This class is for storing and generating the metrics of each algorithm """
    def __init__(self):
        # These are the cumulative values. Useful for the time-based comparison without weight.
        self.name = ""
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

        # These are the values for the current time window only!
        self.cTP = 0 # a
        self.cTN = 0 # d
        self.cFP = 0 # c
        self.cFN = 0 # b
        self.cB1 = 0 # Predicted negative and real was background
        self.cB2 = 0 # Predicted positive and real was background
        self.cB3 = 0 # Predicted background and real was negative
        self.cB4 = 0 # Predicted background and real was positive
        self.cB5 = 0 # Predicted background and real was background
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

        # These are the cumulative weighted values
        self.t_TP = 0 # a
        self.t_TN = 0 # d
        self.t_FP = 0 # c
        self.t_FN = 0 # b
        self.t_B1 = 0 # Predicted negative and real was background
        self.t_B2 = 0 # Predicted positive and real was background
        self.t_B3 = 0 # Predicted background and real was negative
        self.t_B4 = 0 # Predicted background and real was positive
        self.t_B5 = 0 # Predicted background and real was background
        self.t_TPR = -1
        self.t_TNR = -1
        self.t_FNR = -1
        self.t_FPR = -1
        self.t_Accuracy = -1
        self.t_Precision = -1
        self.t_ErrorRate = -1
        self.t_fmeasure1 = -1
        self.t_fmeasure2 = -1
        self.t_fmeasure05 = -1

        # These are the weighted values for the current time window only!
        self.ct_TP = 0 # a
        self.ct_TN = 0 # d
        self.ct_FP = 0 # c
        self.ct_FN = 0 # b
        self.ct_B1 = 0 # Predicted negative and real was background
        self.ct_B2 = 0 # Predicted positive and real was background
        self.ct_B3 = 0 # Predicted background and real was negative
        self.ct_B4 = 0 # Predicted background and real was positive
        self.ct_B5 = 0 # Predicted background and real was background
        self.ct_TPR = -1
        self.ct_TNR = -1
        self.ct_FNR = -1
        self.ct_FPR = -1
        self.ct_Accuracy = -1
        self.ct_Precision = -1
        self.ct_ErrorRate = -1
        self.ct_fmeasure1 = -1
        self.ct_fmeasure2 = -1
        self.ct_fmeasure05 = -1

        # Which column does this alg use in the input line?
        self.headercolumn = -1
        # The algorithm's valid labels. [NegativeLabel, PositiveLabel, BackgroundLabel ]. So self.algorithm_labels[0] is the negative label, 
        # and self.algorithm_labels[1] is the positive label and self.algorithm_labels[2] is the background label. Background label is optional.
        self.algorithm_labels = {}

        # The file real labels. [0] is Normal Label, [1] is Botnet label, [2] is Background label. There is ONLY ONE label for each category. 
        # Can not be two normal labels. In the past we had both 'Normal' and 'Legitimate' as normal labels. BEWARE! Check your file!
        self.real_labels = {}

        # Vectors for plotting common errors
        self.plotTP = []
        self.plotTN = []
        self.plotFP = []
        self.plotFN = []
        self.plotTPR = []
        self.plotTNR = []
        self.plotFNR = []
        self.plotFPR = []
        self.plotAccuracy = []
        self.plotPrecision = []
        self.plotErrorRate = []
        self.plotfmeasure1 = []
        self.plotfmeasure2 = []
        self.plotfmeasure05 = []
        # Vectors for plotting weighted errors
        self.t_plotTP = []
        self.t_plotTN = []
        self.t_plotFP = []
        self.t_plotFN = []
        self.t_plotTPR = []
        self.t_plotTNR = []
        self.t_plotFNR = []
        self.t_plotFPR = []
        self.t_plotAccuracy = []
        self.t_plotPrecision = []
        self.t_plotErrorRate = []
        self.t_plotfmeasure1 = []
        self.t_plotfmeasure2 = []
        self.t_plotfmeasure05 = []

        # This will store a label for each IP address seen for this algorithm in the current time window. This is the final label for that ip.
        self.ip_labels = {}
        # This will store the current label seen for each IP address in the current time window. This label is not the final decision.
        self.ip_current_labels = {}

    def clean_current_errors(self):
        """ Clean the errors for the current time window and the weighted errors. Do not delete the cumulative values """
        try:
            # These are the values for the current time window only!
            self.cTP = 0 # a
            self.cTN = 0 # d
            self.cFP = 0 # c
            self.cFN = 0 # b
            self.cB1 = 0 # Predicted negative and real was background
            self.cB2 = 0 # Predicted positive and real was background
            self.cB3 = 0 # Predicted background and real was negative
            self.cB4 = 0 # Predicted background and real was positive
            self.cB5 = 0 # Predicted background and real was background
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

            # These are the weighted value for the current time window only!
            self.ct_TP = 0 # a
            self.ct_TN = 0 # d
            self.ct_FP = 0 # c
            self.ct_FN = 0 # b
            self.ct_B1 = 0 # Predicted negative and real was background
            self.ct_B2 = 0 # Predicted positive and real was background
            self.ct_B3 = 0 # Predicted background and real was negative
            self.ct_B4 = 0 # Predicted background and real was positive
            self.ct_B5 = 0 # Predicted background and real was background
            self.ct_TPR = -1
            self.ct_TNR = -1
            self.ct_FNR = -1
            self.ct_FPR = -1
            self.ct_Accuracy = -1
            self.ct_Precision = -1
            self.ct_ErrorRate = -1
            self.ct_fmeasure1 = -1
            self.ct_fmeasure2 = -1
            self.ct_fmeasure05 = -1

        except Exception as inst:
            if debug:
                print ('Some problem in clean_current_errors() method of class algorithm')
            print (type(inst))     # the exception instance
            print (inst.args)      # arguments stored in .args
            print (inst)           # __str__ allows args to printed directly
            x, y = inst          # __getitem__ allows args to be unpacked directly
            print ('x =', x)
            print ('y =', y)
            exit(-1)


    def __repr__(self):
        """ Default printing method """ 
        return repr('{0} TP={1}, TN={2}, FP={3}, FN={4} TPR={5:.2f}, TNR={6:.2f}, FPR={7:.2f}, FNR={8:.2f}, Precision={9:.2f}, Accuracy={10:.2f}, ErrorRate={11:.2f}, FM1={12:.2f}, FM2={13:.2f}, FM05={14:.2f}'.format(self.name, self.TP, self.TN, self.FP, self.FN, self.TPR, self.TNR, self.FPR, self.FNR, self.Precision, self.Accuracy, self.ErrorRate, self.fmeasure1, self.fmeasure2, self.fmeasure05))

    def compute_error(self, predictedlabel, reallabel):
        """ Get the predicted label and the real label and compute the error type. Also verifies that labels are valid for this algorithm """
        global debug
        try:
            if debug:
                print (' > Computing errors for algorithm: {0}'.format(self.name))
            # Verify that the new label is valid
            # The final 'or' is to accept labels that have a number at the end like 'Botnet6'
            if (predictedlabel in self.algorithm_labels.values() and reallabel in self.real_labels.values()) or predictedlabel[:-1] in self.algorithm_labels.values() or predictedlabel[:-2] in self.algorithm_labels.values():
                # They are valid

                # Is it the negative label?
                #if self.algorithm_labels[0] == predictedlabel :
                if self.algorithm_labels[0] in predictedlabel :
                    # This algorithm said Negative 

                    #if reallabel == self.real_labels[0]:
                    if self.real_labels[0] in reallabel:
                        # Real is Normal. True Negative.
                        self.addTN()
                        if debug or verbose:
                            print ('\tReal Label: \x1b\x5b1;33;40m{0}\x1b\x5b0;0;40m, {1}: {2}. Decision \x1b\x5b1;33;40mTN\x1b\x5b0;0;40m'.format(reallabel, self.name, predictedlabel))

                    #elif reallabel == self.real_labels[1]:
                    elif self.real_labels[1] in reallabel:
                        # Real is Botnet. False Negative.
                        self.addFN()
                        if debug or verbose:
                            print ('\tReal Label: \x1b\x5b1;31;40m{0}\x1b\x5b0;0;40m, {1}: {2}. Decision: \x1b\x5b1;31;40mFN\x1b\x5b0;0;40m'.format(reallabel, self.name, predictedlabel))

                    #elif reallabel == self.real_labels[2]:
                    elif self.real_labels[2] in reallabel:
                        # Real is Background.
                        self.addB1()
                        if debug:
                            print ('\t\tBackground1')

                # Is it the positive label?
                # This comparison is to catch 'Botnet6' predicted label correctly as 'Botnet' real label.
                # Should not catch CAMNEP labels
                elif self.algorithm_labels[1] in predictedlabel:
                    # This algorithm said Positive 

                    #if reallabel == self.real_labels[0]:
                    if self.real_labels[0] in reallabel: 
                        # Real is Normal. False Positive
                        self.addFP()
                        if debug or verbose:
                            print ('\tReal Label: \x1b\x5b1;31;40m{0}\x1b\x5b0;0;40m, {1}: {2}. Decision: \x1b\x5b1;31;40mFP\x1b\x5b0;0;40m'.format(reallabel, self.name, predictedlabel))

                    #elif reallabel == self.real_labels[1]:
                    elif self.real_labels[1] in reallabel:
                        # Real is Botnet. True Positive.
                        self.addTP()
                        if debug or verbose:
                            print ('\tReal Label: \x1b\x5b1;33;40m{0}\x1b\x5b0;0;40m, {1}: {2}. Decision \x1b\x5b1;33;40mTP\x1b\x5b0;0;40m'.format(reallabel, self.name, predictedlabel))

                    #elif reallabel == self.real_labels[2]:
                    elif self.real_labels[2] in reallabel:
                        # Real is Background. 
                        self.addB2()
                        if debug:
                            print ('\t\tBackground2')

                # Is it the background label?
                #elif self.algorithm_labels[2] == predictedlabel :
                elif self.algorithm_labels[2] in predictedlabel :
                    # This algorithm said Background 

                    #if reallabel == self.real_labels[0]:
                    if self.real_labels[0] in reallabel:
                        # Real is Normal.
                        self.addB3()
                        if debug:
                            print ('\t\tBackground3')

                    #elif reallabel == self.real_labels[1]:
                    elif self.real_labels[1] in reallabel:
                        # Real is Botnet.
                        self.addB4()
                        if debug:
                            print ('\t\tBackground4')

                    #elif reallabel == self.real_labels[2]:
                    elif self.real_labels[2] in reallabel:
                        # Real is Background. 
                        self.addB5()
                        if debug:
                            print ('\t\tBackground5')

            else:
                # They are not valid
                print ('WARNING! An invalid label was given for algorithm {0}: Algorithm accepted labels:{1}, algorithm predicted label:{2}. Real accepted labels:{3}, given real label: {4}'.format(self.name, self.algorithm_labels, predictedlabel, self.real_labels, reallabel))
                exit(-1)
        except Exception as inst:
            if debug:
                print ('Some problem in compute_error() method of class algorithm')
            print (type(inst))     # the exception instance
            print (inst.args)      # arguments stored in .args
            print (inst)           # __str__ allows args to printed directly
            x, y = inst          # __getitem__ allows args to be unpacked directly
            print ('x =', x)
            print ('y =', y)
            exit(-1)


    def reportprint(self, longest_name):
        """ The reported values """ 
        # I still did not found out how to use longest_name to change the width of the columns...
        text = '{0:30} TP={1:8}, TN={2:8}, FP={3:8}, FN={4:8}, TPR={5:.3f}, TNR={6:.3f}, FPR={7:.3f}, FNR={8:.3f}, Precision={9:7.4f}, Accuracy={10:5.4f}, ErrorRate={11:5.3f}, FM1={12:7.4f}, FM2={13:7.4f}, FM05={14:7.4f}, B1={15:8}, B2={16:8}, B3={17:3}, B4={18:3}, B5={19:3}'.format(self.name, self.TP, self.TN, self.FP, self.FN, self.TPR, self.TNR, self.FPR, self.FNR, self.Precision, self.Accuracy, self.ErrorRate, self.fmeasure1, self.fmeasure2, self.fmeasure05, self.B1, self.B2, self.B3, self.B4, self.B5)
        print (text)

    def report_CSV_print(self, longest_name, csv_handler):
        """ The reported values in csv format """ 
        # I still did not found out how to use longest_name to change the width of the columns...
        text = '{0:30},{1:8},{2:8},{3:8},{4:8},{5:.3f},{6:.3f},{7:.3f},{8:.3f},{9:7.4f},{10:5.4f},{11:5.3f},{12:7.4f},{13:7.4f},{14:7.4f},{15:8},{16:8},{17:3},{18:3},{19:3}'.format(self.name, self.TP, self.TN, self.FP, self.FN, self.TPR, self.TNR, self.FPR, self.FNR, self.Precision, self.Accuracy, self.ErrorRate, self.fmeasure1, self.fmeasure2, self.fmeasure05, self.B1, self.B2, self.B3, self.B4, self.B5)
        csv_handler.write(text+'\n')

    def current_reportprint(self, longest_name):
        """ The reported values """ 
        # I still did not found out how to use longest_name to change the width of the columns...
        print ('{0:30} TP={1:8}, TN={2:8}, FP={3:8}, FN={4:8}, TPR={5:.3f}, TNR={6:.3f}, FPR={7:.3f}, FNR={8:.3f}, Precision={9:7.4f}, Accuracy={10:5.4f}, ErrorRate={11:5.3f}, FM1={12:7.4f}, FM2={13:7.4f}, FM05={14:7.4f}, B1={15:8}, B2={16:8}, B3={17:3}, B4={18:3}, B5={19:3}'.format(self.name, self.cTP, self.cTN, self.cFP, self.cFN, self.cTPR, self.cTNR, self.cFPR, self.cFNR, self.cPrecision, self.cAccuracy, self.cErrorRate, self.cfmeasure1, self.cfmeasure2, self.cfmeasure05, self.cB1, self.cB2, self.cB3, self.cB4, self.cB5))

    def weighted_reportprint(self, longest_name):
        """ The reported values """ 
        # I still did not found out how to use longest_name to change the width of the columns...
        text = '{0:30} t-TP={1:.4f}, t-TN={2:8}, t-FP={3:8}, t-FN={4:.4f}, t-TPR={5:.3f}, t-TNR={6:.3f}, t-FPR={7:.3f}, t-FNR={8:.3f}, t-Precision={9:7.4f}, t-Accuracy={10:5.4f}, t-ErrorRate={11:5.3f}, t-FM1={12:7.4f}, t-FM2={13:7.4f}, t-FM05={14:7.4f}, t-B1={15:8}, t-B2={16:8}, t-B3={17:3}, t-B4={18:3}, t-B5={19:3}'.format(self.name, self.t_TP, self.t_TN, self.t_FP, self.t_FN, self.t_TPR, self.t_TNR, self.t_FPR, self.t_FNR, self.t_Precision, self.t_Accuracy, self.t_ErrorRate, self.t_fmeasure1, self.t_fmeasure2, self.t_fmeasure05, self.t_B1, self.t_B2, self.t_B3, self.t_B4, self.t_B5)
        print (text)

    def weighted_report_CSV_print(self, longest_name, csv_handler):
        """ The reported values """ 
        # If there is a csv file, write on it
        # I still did not found out how to use longest_name to change the width of the columns...
        text = '{0:30},{1:.4f},{2:8},{3:8},{4:.4f},{5:.3f},{6:.3f},{7:.3f},{8:.3f},{9:7.4f},{10:5.4f},{11:5.3f},{12:7.4f},{13:7.4f},{14:7.4f},{15:8},{16:8},{17:3},{18:3},{19:3}'.format(self.name, self.t_TP, self.t_TN, self.t_FP, self.t_FN, self.t_TPR, self.t_TNR, self.t_FPR, self.t_FNR, self.t_Precision, self.t_Accuracy, self.t_ErrorRate, self.t_fmeasure1, self.t_fmeasure2, self.t_fmeasure05, self.t_B1, self.t_B2, self.t_B3, self.t_B4, self.t_B5)
        csv_handler.write(text+'\n')

    def weighted_current_reportprint(self, longest_name):
        """ The reported values """ 
        # I still did not found out how to use longest_name to change the width of the columns...
        print ('{0:30} t-TP={1:.4f}, t-TN={2:8}, t-FP={3:8}, t-FN={4:.4f}, t-TPR={5:.3f}, t-TNR={6:.3f}, t-FPR={7:.3f}, t-FNR={8:.3f}, t-Precision={9:7.4f}, t-Accuracy={10:5.4f}, t-ErrorRate={11:5.3f}, t-FM1={12:7.4f}, t-FM2={13:7.4f}, t-FM05={14:7.4f}, t-B1={15:8}, t-B2={16:8}, t-B3={17:3}, t-B4={18:3}, t-B5={19:3}'.format(self.name, self.ct_TP, self.ct_TN, self.ct_FP, self.ct_FN, self.ct_TPR, self.ct_TNR, self.ct_FPR, self.ct_FNR, self.ct_Precision, self.ct_Accuracy, self.ct_ErrorRate, self.ct_fmeasure1, self.ct_fmeasure2, self.ct_fmeasure05, self.ct_B1, self.ct_B2, self.ct_B3, self.ct_B4, self.ct_B5))

    def addB1(self):
        """ Predicted negative but real was background """ 
        self.B1 = self.B1 + 1
        self.cB1 = self.cB1 + 1

    def addB2(self):
        """ Predicted positive but real was background """ 
        self.B2 = self.B2 + 1
        self.cB2 = self.cB2 + 1

    def addB3(self):
        """ Predicted background and real was negative """ 
        self.B3 = self.B3 + 1
        self.cB3 = self.cB3 + 1

    def addB4(self):
        """ Predicted background and real was positive """ 
        self.B4 = self.B4 + 1
        self.cB4 = self.cB4 + 1

    def addB5(self):
        """ Predicted background and real was background """ 
        self.B5 = self.B5 + 1
        self.cB5 = self.cB5 + 1

    def addTP(self):
        """ Add a True positive to this algorithm """ 
        self.TP = self.TP + 1
        self.cTP = self.cTP + 1
        self.computeMetrics()

    def addTN(self):
        """ Add a True negative to this algorithm """ 
        self.TN = self.TN + 1
        self.cTN = self.cTN + 1
        self.computeMetrics()

    def addFP(self):
        """ Add a False positive to this algorithm """ 
        self.FP = self.FP + 1
        self.cFP = self.cFP + 1
        self.computeMetrics()

    def addFN(self):
        """ Add a False negative to this algorithm """ 
        self.FN = self.FN + 1
        self.cFN = self.cFN + 1
        self.computeMetrics()

    def updateplot(self):
        """ Update the plot with the new values """ 
        self.plotTP.append(self.TP)
        self.plotTN.append(self.TN)
        self.plotFP.append(self.FP)
        self.plotFN.append(self.FN)
        self.plotTPR.append(self.TPR)
        self.plotTNR.append(self.TNR)
        self.plotFPR.append(self.FPR)
        self.plotFNR.append(self.FNR)
        self.plotPrecision.append(self.Precision)
        self.plotAccuracy.append(self.Accuracy)
        self.plotErrorRate.append(self.ErrorRate)
        self.plotfmeasure1.append(self.fmeasure1)
        self.plotfmeasure2.append(self.fmeasure2)
        self.plotfmeasure05.append(self.fmeasure05)

    def update_weighted_plot(self):
        """ Update the plot with the new values """ 
        self.t_plotTP.append(self.t_TP)
        self.t_plotTN.append(self.t_TN)
        self.t_plotFP.append(self.t_FP)
        self.t_plotFN.append(self.t_FN)
        self.t_plotTPR.append(self.t_TPR)
        self.t_plotTNR.append(self.t_TNR)
        self.t_plotFPR.append(self.t_FPR)
        self.t_plotFNR.append(self.t_FNR)
        self.t_plotPrecision.append(self.t_Precision)
        self.t_plotAccuracy.append(self.t_Accuracy)
        self.t_plotErrorRate.append(self.t_ErrorRate)
        self.t_plotfmeasure1.append(self.t_fmeasure1)
        self.t_plotfmeasure2.append(self.t_fmeasure2)
        self.t_plotfmeasure05.append(self.t_fmeasure05)

    def compute_weighted_metrics(self, correcting_function, amount_of_unique_ips):
        """ Compute the weighted metrics. Receives the correcting_function value and the amount of labels in the current time window """ 
        # t-tp score
        try:
            # Current value
            for rl in amount_of_unique_ips:
                # 1 is for the positive class or botnet class here
                if self.real_labels[1] in rl:
                    temp = amount_of_unique_ips[rl]
                    break
                else:
                    temp = 0

            #self.ct_TP = ( self.cTP * float(correcting_function) ) / amount_of_unique_ips[self.real_labels[1]]
            self.ct_TP = ( self.cTP * float(correcting_function) ) / temp
            # Cumulative value
            self.t_TP = self.t_TP + self.ct_TP
        except ZeroDivisionError:
            # ValueError was for dividing by 0. KeyError was if we still have no amount of ips with that label
            pass
        except (KeyError, ValueError):
            if debug:
                print ('WARNING, something is broken on compute_weighted_metrics')

        # t-fn score
        try:
            for rl in amount_of_unique_ips:
                # 1 is for the positive class or botnet class here
                if self.real_labels[1] in rl:
                    temp = amount_of_unique_ips[rl]
                    break
                else:
                    temp = 0
            #self.ct_FN = ( self.cFN * float(correcting_function) ) / amount_of_unique_ips[self.real_labels[1]]
            self.ct_FN = ( self.cFN * float(correcting_function) ) / temp
            self.t_FN = self.t_FN + self.ct_FN
        except ZeroDivisionError:
            # ValueError was for dividing by 0. KeyError was if we still have no amount of ips with that label
            pass
        except (KeyError, ValueError):
            if debug:
                print ('WARNING, something is broken on compute_weighted_metrics')

        # t-fp score. 0 is normal ips
        try:
            for rl in amount_of_unique_ips:
                if self.real_labels[0] in rl:
                    temp = float(amount_of_unique_ips[rl])
                    break
                else:
                    temp = 0
            #self.ct_FP = self.cFP / float(amount_of_unique_ips[self.real_labels[0]])
            self.ct_FP = self.cFP / temp
            self.t_FP = self.t_FP + self.ct_FP
        except ZeroDivisionError:
            # ValueError was for dividing by 0. KeyError was if we still have no amount of ips with that label
            pass
        except (KeyError, ValueError):
            if debug:
                print ('WARNING, something is broken on compute_weighted_metrics')

        # t-tn score. 0 is normal ips
        try:
            for rl in amount_of_unique_ips:
                if self.real_labels[0] in rl:
                    temp = float(amount_of_unique_ips[rl])
                    break
                else:
                    temp = 0
            #self.ct_TN = self.cTN / float(amount_of_unique_ips[self.real_labels[0]])
            self.ct_TN = self.cTN / temp
            self.t_TN = self.t_TN + self.ct_TN
        except ZeroDivisionError:
            # ValueError was for dividing by 0. KeyError was if we still have no amount of ips with that label
            pass
        except (KeyError, ValueError):
            if debug:
                print ('WARNING, something is broken on compute_weighted_metrics')


        # t-b1 score. 2 is background ips
        try:
            for rl in amount_of_unique_ips:
                if self.real_labels[2] in rl:
                    temp = float(amount_of_unique_ips[rl])
                    break
                else:
                    temp = 0
            #self.ct_B1 = self.cB1 / float(amount_of_unique_ips[self.real_labels[2]])
            self.ct_B1 = self.cB1 / temp
            self.t_B1 = self.t_B1 + self.ct_B1
        except ZeroDivisionError:
            # ValueError was for dividing by 0. KeyError was if we still have no amount of ips with that label
            pass
        except (KeyError, ValueError):
            if debug:
                print ('WARNING, something is broken on compute_weighted_metrics')

        # t-b2 score. 2 is background ips
        try:
            for rl in amount_of_unique_ips:
                if self.real_labels[2] in rl:
                    temp = float(amount_of_unique_ips[rl])
                    break
                else:
                    temp = 0
            #self.ct_B2 = self.cB2 / float(amount_of_unique_ips[self.real_labels[2]])
            self.ct_B2 = self.cB2 / temp
            self.t_B2 = self.t_B2 + self.ct_B2
        except ZeroDivisionError:
            # ValueError was for dividing by 0. KeyError was if we still have no amount of ips with that label
            pass
        except (KeyError, ValueError):
            if debug:
                print ('WARNING, something is broken on compute_weighted_metrics')

        # t-b3 score. 2 is background ips
        try:
            for rl in amount_of_unique_ips:
                if self.real_labels[2] in rl:
                    temp = float(amount_of_unique_ips[rl])
                    break
                else:
                    temp = 0
            #self.ct_B3 = self.cB3 / float(amount_of_unique_ips[self.real_labels[2]])
            self.ct_B3 = self.cB3 / temp
            self.t_B3 = self.t_B3 + self.ct_B3
        except ZeroDivisionError:
            # ValueError was for dividing by 0. KeyError was if we still have no amount of ips with that label
            pass
        except (KeyError, ValueError):
            if debug:
                print ('WARNING, something is broken on compute_weighted_metrics')

        # t-b4 score. 2 is background ips
        try:
            for rl in amount_of_unique_ips:
                if self.real_labels[2] in rl:
                    temp = float(amount_of_unique_ips[rl])
                    break
                else:
                    temp = 0
            #self.ct_B4 = self.cB4 / float(amount_of_unique_ips[self.real_labels[2]])
            self.ct_B4 = self.cB4 / temp
            self.t_B4 = self.t_B4 + self.ct_B4
        except ZeroDivisionError:
            # ValueError was for dividing by 0. KeyError was if we still have no amount of ips with that label
            pass
        except (KeyError, ValueError):
            if debug:
                print ('WARNING, something is broken on compute_weighted_metrics')

        # t-b5 score. 2 is background ips
        try:
            for rl in amount_of_unique_ips:
                if self.real_labels[2] in rl:
                    temp = float(amount_of_unique_ips[rl])
                    break
                else:
                    temp = 0
            #self.ct_B5 = self.cB5 / float(amount_of_unique_ips[self.real_labels[2]])
            self.ct_B5 = self.cB5 / temp
            self.t_B5 = self.t_B5 + self.ct_B5
        except ZeroDivisionError:
            # ValueError was for dividing by 0. KeyError was if we still have no amount of ips with that label
            pass
        except (KeyError, ValueError):
            if debug:
                print ('WARNING, something is broken on compute_weighted_metrics')

        # t_TPR. Also Hit rate, detect rate, Recall or sensitivity. Portion of positives examples the model predicts correctly.
        try:
            self.t_TPR = ( self.t_TP ) / float(self.t_TP + self.t_FN)
        except ZeroDivisionError:
            self.t_TPR = -1
        try:
            self.ct_TPR = ( self.ct_TP ) / float(self.ct_TP + self.ct_FN)
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equal to do nothing.
            pass

        # t_TNR. Also Correct-reject rate or specificity. Portion of negative examples the model predicts correctly.
        try:
            self.t_TNR = ( self.t_TN ) / float( self.t_TN + self.t_FP )
        except ZeroDivisionError:
            self.t_TNR = -1
        try:
            self.ct_TNR = ( self.ct_TN ) / float( self.ct_TN + self.ct_FP )
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equal to do nothing.
            pass

        # t_FPR. Also False-alarm rate. The portion of negative examples that the model wrongly predicts as positive.
        try:
            self.t_FPR = ( self.t_FP ) / float( self.t_TN + self.t_FP )
        except ZeroDivisionError:
            self.t_FPR = -1
        try:
            self.ct_FPR = ( self.ct_FP ) / float( self.ct_TN + self.ct_FP )
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equal to do nothing.
            pass

        # t_FNR. Also Miss rate. Portion of positives examples that the classifier wrongly predicts as negative.
        try:
            self.t_FNR = ( self.t_FN ) / float(self.t_TP + self.t_FN)
        except ZeroDivisionError:
            self.t_FNR = -1
        try:
            self.ct_FNR = ( self.ct_FN ) / float(self.ct_TP + self.ct_FN)
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equal to do nothing.
            pass

        # t_Precision. Portion of all the examples predicted as positives that were really positives.
        try:
            self.t_Precision = ( self.t_TP ) / float(self.t_TP + self.t_FP)
        except ZeroDivisionError:
            self.t_Precision = -1
        try:
            self.ct_Precision = self.ct_TP / float(self.ct_TP + self.ct_FP)
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equal to do nothing.
            pass

        # t_Accuracy. The portion of examples that the model predicts correctly
        try:
            self.t_Accuracy = ( self.t_TP + self.t_TN ) / float( self.t_TP + self.t_TN + self.t_FP + self.t_FN )
        except ZeroDivisionError:
            self.t_Accuracy = -1
        try:
            self.ct_Accuracy = ( self.ct_TP + self.ct_TN ) / float( self.ct_TP + self.ct_TN + self.ct_FP + self.ct_FN )
        except ZeroDivisionError:
            # We should add 0 to the current value, that is equal to do nothing.
            pass

        # t_Error Rate. The portion of examples that the model predicts incorrectly
        try:
            self.t_ErrorRate = ( self.t_FN + self.t_FP ) / float( self.t_TP + self.t_TN + self.t_FP + self.t_FN )
        except ZeroDivisionError:
            self.t_ErrorRate = -1
        try:
            self.ct_ErrorRate = ( self.ct_FN + self.ct_FP ) / float( self.ct_TP + self.ct_TN + self.ct_FP + self.ct_FN )
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
        self.beta = 2
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



    def computeMetrics(self):
        """ Compute the metrics """ 
        # TPR. Also Hit rate, detect rate, Recall or sensitivity. Portion of positives examples the model predicts correctly.
        try:
            self.TPR = (self.TP) / float( self.TP + self.FN )
        except ZeroDivisionError:
            self.TPR = -1
        try:
            self.cTPR = (self.cTP) / float( self.cTP + self.cFN )
        except ZeroDivisionError:
            self.cTPR = -1

        # TNR. Also Correct-reject rate or specificity. Portion of negative examples the model predicts correctly.
        try:
            self.TNR = ( self.TN ) / float( self.TN + self.FP )
        except ZeroDivisionError:
            self.TNR = -1
        try:
            self.cTNR = ( self.cTN ) / float( self.cTN + self.cFP )
        except ZeroDivisionError:
            self.cTNR = -1

        # FPR. Also False-alarm rate. The portion of negative examples that the model wrongly predicts as positive.
        try:
            self.FPR = ( self.FP ) / float( self.TN + self.FP )
        except ZeroDivisionError:
            self.FPR = -1
        try:
            self.cFPR = ( self.cFP ) / float( self.cTN + self.cFP )
        except ZeroDivisionError:
            self.cFPR = -1

        # FNR. Also Miss rate. Portion of positives examples that the classifier wrongly predicts as negative.
        try:
            self.FNR = ( self.FN ) / float( self.TP + self.FN )
        except ZeroDivisionError:
            self.FNR = -1
        try:
            self.cFNR = ( self.cFN ) / float( self.cTP + self.cFN )
        except ZeroDivisionError:
            self.cFNR = -1

        # Precision. Portion of all the examples predicted as positives that were really positives.
        try:
            self.Precision = ( self.TP ) / float( self.TP + self.FP)
        except ZeroDivisionError:
            self.Precision = -1
        try:
            self.cPrecision = ( self.cTP ) / float( self.cTP + self.cFP)
        except ZeroDivisionError:
            self.cPrecision = -1

        # Accuracy. The portion of examples that the model predicts correctly
        try:
            self.Accuracy = ( self.TP + self.TN ) / float( self.TP + self.TN + self.FP + self.FN )
        except ZeroDivisionError:
            self.Accuracy = -1
        try:
            self.cAccuracy = ( self.cTP + self.cTN ) / float( self.cTP + self.cTN + self.cFP + self.cFN )
        except ZeroDivisionError:
            self.cAccuracy = -1

        # Error Rate. The portion of examples that the model predicts incorrectly
        try:
            self.ErrorRate = ( self.FN + self.FP ) / float( self.TP + self.TN + self.FP + self.FN )
        except ZeroDivisionError:
            self.ErrorRate = -1
        try:
            self.cErrorRate = ( self.cFN + self.cFP ) / float( self.cTP + self.cTN + self.cFP + self.cFN )
        except ZeroDivisionError:
            self.cErrorRate = -1

        # F1-Measure.
        self.beta = 1.0
        # With beta=1 F-Measure is also Fscore
        try:
            self.fmeasure1 = ( ( (self.beta * self.beta) + 1 ) * self.Precision * self.TPR  ) / float( ( self.beta * self.beta * self.Precision ) + self.TPR )
        except ZeroDivisionError:
            self.fmeasure1 = -1
        try:
            self.cfmeasure1 = ( ( (self.beta * self.beta) + 1 ) * self.cPrecision * self.cTPR  ) / float( ( self.beta * self.beta * self.cPrecision ) + self.cTPR )
        except ZeroDivisionError:
            self.cfmeasure1 = -1

        # F2-Measure.
        self.beta = 2
        # With beta=2 F-Measure gives more importance to TPR (recall)
        try:
            self.fmeasure2 = ( ( (self.beta * self.beta) + 1 ) * self.Precision * self.TPR  ) / float( ( self.beta * self.beta * self.Precision ) + self.TPR )
        except ZeroDivisionError:
            self.fmeasure2 = -1
        try:
            self.cfmeasure2 = ( ( (self.beta * self.beta) + 1 ) * self.cPrecision * self.cTPR  ) / float( ( self.beta * self.beta * self.cPrecision ) + self.cTPR )
        except ZeroDivisionError:
            self.cfmeasure2 = -1

        # F0.5-Measure.
        self.beta = 0.5
        # With beta=2 F-Measure gives more importance to Precision
        try:
            self.fmeasure05 = ( ( (self.beta * self.beta) + 1 ) * self.Precision * self.TPR  ) / float( ( self.beta * self.beta * self.Precision ) + self.TPR )
        except ZeroDivisionError:
            self.fmeasure05 = -1
        try:
            self.cfmeasure05 = ( ( (self.beta * self.beta) + 1 ) * self.cPrecision * self.cTPR  ) / float( ( self.beta * self.beta * self.cPrecision ) + self.TPR )
        except ZeroDivisionError:
            self.cfmeasure05 = -1

        # Mean squared error?
