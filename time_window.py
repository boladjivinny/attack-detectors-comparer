from . import *

class time_windows():
    """ This class holds all the information of the current time window. The ips, methods, etc. """
    def __init__(self):
        # ID. Starts with zero so we can 
        self.id = 0
        # This will hold each IP address label for this time window
        self.ip_original_labels = {}
        # This will link us to the algorithms
        self.algorithms_dict = {}
        self.TP = 0
        self.TN = 0
        self.FN = 0
        self.FP = 0
        self.B1 = 0
        self.B2 = 0
        self.B3 = 0
        self.B4 = 0
        self.B5 = 0
        self.amount_of_unique_ips = {}
        self.amount_of_labels = {}
        # Self assign a new time window id.
        self.assign_id()
        self.lines_read = 0

    def __repr__(self):
        """ Default printing method """ 
        text= '####################################\nTime Window Number: {0}\nAmount of algorithms being used: {1}\nAmount of unique ips: {2}\nAmount of labels: {3}\nLines read: {4}\n####################################'.format(self.id, len(self.algorithms_dict), self.amount_of_unique_ips, self.amount_of_labels, self.lines_read) 
        return text

    def assign_id(self):
        """ Assign an id to this time window. It is the time window number. """
        global time_window_id
        global debug
        time_window_id = time_window_id + 1
        self.id = time_window_id
        #if debug:
        #    print (' > Time window id:{0}'.format(self.id))

    def clean_ip_labels(self):
        """ Clean the ip labels dict for each algorithm """
        self.ip_original_labels = {}

        for alg in self.algorithms_dict:
            self.algorithms_dict[alg].ip_labels = {}
            self.algorithms_dict[alg].ip_current_labels = {}
            self.algorithms_dict[alg].clean_current_errors()

    def algorithms_labels_for_this_ip(self, ip):
        """ Get an ip and return the list of labels for each algorithm """
        resp = {}
        for alg in self.algorithms_dict:
            try:
                resp[alg] = self.algorithms_dict[alg].ip_labels[ip]
            except KeyError:
                resp[alg] = ''

        return resp

    def add_ip_label(self, ip, label):
        """ Get an ip and the real label. Check if the ip is new in this time window. Store the label. If it is new, initializate the label for each algorithm"""
        global debug
        try:
            if ip in self.ip_original_labels:
                # We have already seen this ip
                #if debug:
                    #print (' > We have already seen this ip: {0}'.format(ip))

                # Did the real label changed? Verify if it needs to be changed or not according to our strategy.
                if self.ip_original_labels[ip] != label:
                    if 'background' in self.ip_original_labels[ip].lower() and 'botnet' in label.lower():
                        if debug:
                            print ('\nThe label for this IP has changed in the same time window from {0} to {1}!'.format(self.ip_original_labels[ip], label))
                        # Decrease the amount of ips for the previous label
                        self.amount_of_unique_ips[self.ip_original_labels[ip]] -= 1
                        # Increase the amount of ips for the new label
                        try:
                            self.amount_of_unique_ips[label] += 1
                        except KeyError:
                            self.amount_of_unique_ips[label] = 1
                        # Assign the new label to the ip
                        self.ip_original_labels[ip] = label

                    elif 'normal' in self.ip_original_labels[ip].lower() and 'botnet' in label.lower(): 
                        if debug:
                            print ('\nThe label for this IP has changed in the same time window from {0} to {1}!!'.format(self.ip_original_labels[ip], label))
                        # Decrease the amount of ips for the previous label
                        self.amount_of_unique_ips[self.ip_original_labels[ip]] -= 1
                        # Increase the amount of ips for the new label
                        try:
                            self.amount_of_unique_ips[label] += 1
                        except KeyError:
                            self.amount_of_unique_ips[label] = 1
                        # Assign the new label to the ip
                        self.ip_original_labels[ip] = label
                    elif 'background' in self.ip_original_labels[ip].lower() and 'normal' in label.lower() and 'from' in label.lower(): 
                        if debug:
                            print ('\nThe label for this IP has changed in the same time window from {0} to {1}!!!'.format(self.ip_original_labels[ip], label))
                        # Decrease the amount of ips for the previous label
                        self.amount_of_unique_ips[self.ip_original_labels[ip]] -= 1
                        # Increase the amount of ips for the new label
                        try:
                            self.amount_of_unique_ips[label] += 1
                        except KeyError:
                            self.amount_of_unique_ips[label] = 1
                        # Assign the new label to the ip
                        self.ip_original_labels[ip] = label
                    elif 'botnet' in self.ip_original_labels[ip].lower() and 'cc' not in self.ip_original_labels[ip].lower() and 'cc' in label.lower(): 
                        if debug:
                            print ('\nThe label for this IP has changed in the same time window from {0} to {1}!!!!'.format(self.ip_original_labels[ip], label))
                        # Decrease the amount of ips for the previous label
                        self.amount_of_unique_ips[self.ip_original_labels[ip]] -= 1
                        # Increase the amount of ips for the new label
                        try:
                            self.amount_of_unique_ips[label] += 1
                        except KeyError:
                            self.amount_of_unique_ips[label] = 1
                        # Assign the new label to the ip
                        self.ip_original_labels[ip] = label


                # Did the label of the algorithms change?
                for alg in self.algorithms_dict:
                    if self.algorithms_dict[alg].ip_labels[ip] != self.algorithms_dict[alg].ip_current_labels[ip]:
                        # Yes. The algorithm changed the label.

                        # If the previous predicted label does not include the positive label for this alg and the new predicted label includes the positive label for this alg, then the new predicted should be the taken into account.

                        #if self.algorithms_dict[alg].ip_labels[ip] != self.algorithms_dict[alg].algorithm_labels[1] and self.algorithms_dict[alg].ip_current_labels[ip] == self.algorithms_dict[alg].algorithm_labels[1]:
                        if self.algorithms_dict[alg].algorithm_labels[1] not in self.algorithms_dict[alg].ip_labels[ip] and self.algorithms_dict[alg].algorithm_labels[1] in self.algorithms_dict[alg].ip_current_labels[ip]:
                            # Yes. We should change the previous predicted label to the new predicted label
                            if debug:
                                print (' > In alg {0}, for ip {1} the label changed from {2} to {3}.'.format(self.algorithms_dict[alg].name, ip, self.algorithms_dict[alg].ip_labels[ip], self.algorithms_dict[alg].ip_current_labels[ip]))

                            self.algorithms_dict[alg].ip_labels[ip] = self.algorithms_dict[alg].ip_current_labels[ip]

            else:
                # We did not see this ip yet. It is new

                # Is the new label a valid one?
                # Note that every algorithm has the real_labels dict on them. We took the labels for AllPositive
                #if debug:
                    #print (' > First time we see this ip: {0}'.format(ip))

                #if label in self.algorithms_dict['AllPositive'].real_labels.values():
                # It is valid

                # Assign it to the ip
                self.ip_original_labels[ip] = label

                # Add 1 to the amount of different ips seen

                # Store the amount of unique ips for each label
                try:
                    self.amount_of_unique_ips[label] += 1
                except KeyError:
                    self.amount_of_unique_ips[label] = 1

                # Assign the predicted label of each algorithm as the final label for this ip for the algorithm. As this is the first time we see this ip, there is no conflict.
                for alg in self.algorithms_dict:
                    self.algorithms_dict[alg].ip_labels[ip] = self.algorithms_dict[alg].ip_current_labels[ip]

                #if debug:
                    #print (' > New ip found: {0}. Real label: {1}.'.format(ip, label))

        except Exception as inst:
            if debug:
                print ('Some problem in add_ip_label() method of class time_window')
            print (type(inst))     # the exception instance
            print (inst.args)      # arguments stored in .args
            print (inst)           # __str__ allows args to printed directly
            x, y = inst          # __getitem__ allows args to be unpacked directly
            print ('x =', x)
            print ('y =', y)
            exit(-1)


    def compute_weighted_errors(self):
        """ For each algorithm in this time window compute weigthed errors """
        global debug
        global alpha
        global first_sum
        global second_sum

        try:
            if debug:
                print ('\n > Compute weighted errors')

            correcting_function = np.exp( -alpha * ( self.id + first_sum ) ) + second_sum

            if debug:
                print (' > Correcting function for time window {0}: {1}'.format(self.id, correcting_function))
                #for alg in self.algorithms_dict:
                    #print (alg)
                    #print ('\t Ip labels: {0}'.format(self.algorithms_dict[alg].ip_labels))
                    #print ('\t Ip Original labels: {0}'.format(self.algorithms_dict[alg].algorithm_labels))
                    #print ('\t Ip Real labels: {0}'.format(self.algorithms_dict[alg].real_labels))
                    #print ('\t'), self.algorithms_dict[alg].current_reportprint(30)

            # Compute and Store the weighted values
            for alg in self.algorithms_dict:
                self.algorithms_dict[alg].compute_weighted_metrics(correcting_function, self.amount_of_unique_ips)


        except Exception as inst:
            if debug:
                print ('Some problem in compute_weighted_errors() method of class time_window')
            print (type(inst))     # the exception instance
            print (inst.args)      # arguments stored in .args
            print (inst)           # __str__ allows args to printed directly
            x, y = inst          # __getitem__ allows args to be unpacked directly
            print ('x =', x)
            print ('y =', y)
            exit(-1)



    def compute_errors(self):
        """ Get the real label and the label of each algorithm and compute the errors"""
        global debug

        try:
            if debug or verbose:
                print ('\nRunning metrics...')
            for alg in self.algorithms_dict:
                # for each algorithm

                # For each ip
                for ip in self.ip_original_labels:
                    # The real label
                    reallabel = self.ip_original_labels[ip]

                    # The algorithms predicted label
                    predictedlabel = self.algorithms_dict[alg].ip_labels[ip]

                    if debug:
                        print (' > Computing errors for algorithm: {0}. Ip: {1}. Real label: {2}. Predicted label: {3}'.format( alg, ip, reallabel, predictedlabel))

                    # Is the predicted label the negative label?
                    #if self.algorithms_dict[alg].algorithm_labels[0] == predictedlabel :
                    if self.algorithms_dict[alg].algorithm_labels[0] in predictedlabel :
                        # This algorithm said Negative 

                        #if reallabel == self.algorithms_dict[alg].real_labels[0]:
                        if self.algorithms_dict[alg].real_labels[0] in reallabel:
                            # Real is Normal. True Negative.
                            self.algorithms_dict[alg].addTN()
                            if debug or verbose:
                                print ('\tReal Label: \x1b\x5b1;33;40m{0}\x1b\x5b0;0;40m, {1}: {2}. Decision \x1b\x5b1;33;40mTN\x1b\x5b0;0;40m'.format(reallabel, self.algorithms_dict[alg].name, predictedlabel))

                        #elif reallabel == self.algorithms_dict[alg].real_labels[1]:
                        elif self.algorithms_dict[alg].real_labels[1] in reallabel:
                            # Real is Botnet. False Negative.
                            self.algorithms_dict[alg].addFN()
                            if debug or verbose:
                                print ('\tReal Label: \x1b\x5b1;31;40m{0}\x1b\x5b0;0;40m, {1}: {2}. Decision: \x1b\x5b1;31;40mFN\x1b\x5b0;0;40m'.format(reallabel, self.algorithms_dict[alg].name, predictedlabel))

                        #elif reallabel == self.algorithms_dict[alg].real_labels[2]:
                        elif self.algorithms_dict[alg].real_labels[2] in reallabel:
                            # Real is Background. 
                            self.algorithms_dict[alg].addB1()

                    # Is the predicted label the positive label?
                    # This comparison is to catch 'Botnet6' predicted label correctly as 'Botnet' real label.
                    # Should not catch CAMNEP labels
                    elif self.algorithms_dict[alg].algorithm_labels[1] in predictedlabel:
                        # This algorithm said Positive 

                        #if reallabel == self.algorithms_dict[alg].real_labels[0]:
                        if self.algorithms_dict[alg].real_labels[0] in reallabel:
                            # Real is Normal. False Positive
                            self.algorithms_dict[alg].addFP()
                            if debug or verbose:
                                print ('\tReal Label: \x1b\x5b1;31;40m{0}\x1b\x5b0;0;40m, {1}: {2}. Decision: \x1b\x5b1;31;40mFP\x1b\x5b0;0;40m'.format(reallabel, self.algorithms_dict[alg].name, predictedlabel))

                        #elif reallabel == self.algorithms_dict[alg].real_labels[1]:
                        elif self.algorithms_dict[alg].real_labels[1] in reallabel:
                            # Real is Botnet. True Positive.
                            self.algorithms_dict[alg].addTP()
                            if debug or verbose:
                                print ('\tReal Label: \x1b\x5b1;33;40m{0}\x1b\x5b0;0;40m, {1}: {2}. Decision \x1b\x5b1;33;40mTP\x1b\x5b0;0;40m'.format(reallabel, self.algorithms_dict[alg].name, predictedlabel))

                        #elif reallabel == self.algorithms_dict[alg].real_labels[2]:
                        elif self.algorithms_dict[alg].real_labels[2] in reallabel:
                            # Real is Background.
                            self.algorithms_dict[alg].addB2()

                    # Is it the background label?
                    #elif self.algorithms_dict[alg].algorithm_labels[2] == predictedlabel :
                    elif self.algorithms_dict[alg].algorithm_labels[2] in predictedlabel :
                        # This algorithm said Background 

                        #if reallabel == self.algorithms_dict[alg].real_labels[0]:
                        if self.algorithms_dict[alg].real_labels[0] in reallabel:
                            # Real is Normal. 
                            self.algorithms_dict[alg].addB3()

                        #elif reallabel == self.algorithms_dict[alg].real_labels[1]:
                        elif self.algorithms_dict[alg].real_labels[1] in reallabel:
                            # Real is Botnet.
                            #self.algorithms_dict[alg].addB4()

                            # Not sure if counting a FN here is ok.
                            # Real is Botnet. False Negative.
                            self.algorithms_dict[alg].addFN()
                            if debug or verbose:
                                print ('\tReal Label: \x1b\x5b1;31;40m{0}\x1b\x5b0;0;40m, {1}: {2}. Decision: \x1b\x5b1;31;40mFN\x1b\x5b0;0;40m'.format(reallabel, self.algorithms_dict[alg].name, predictedlabel))

                        #elif reallabel == self.algorithms_dict[alg].real_labels[2]:
                        elif self.algorithms_dict[alg].real_labels[2] in reallabel:
                            # Real is Background.
                            self.algorithms_dict[alg].addB5()

        except Exception as inst:
            if debug:
                print ('Some problem in compute_error() method of class time_window')
            print (type(inst))     # the exception instance
            print (inst.args)      # arguments stored in .args
            print (inst)           # __str__ allows args to printed directly
            x, y = inst          # __getitem__ allows args to be unpacked directly
            print ('x =', x)
            print ('y =', y)
            exit(-1)