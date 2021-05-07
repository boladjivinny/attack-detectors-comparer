from datetime import datetime

from . import *

def plot(file, time_window, comparison_type, time_windows_group):
    """
    For ploting the performance metrics of all methods. time_window and file are only for the title.
    """
    try:
        import matplotlib.pyplot as plt
        global time_window_id # Here it is equal to the amount of time windows
        global plot_file
        global alpha

        if debug:
            print (' > Plotting the metrics...')

        # It does not catch up things like 0.4%
        percentage_of_the_file_tested = ""

        # We should plot all the metrics against the number of interval. From 1 
        range_time_windows = range(1, time_window_id + 1)
        
        if comparison_type == 'time':
            # We only work with bclus and CAMNEP here, we can not plot everything.
            clusterAlg = time_windows_group[-1].algorithms_dict['Bclus']
            #camnepAlg = time_windows_group[-1].algorithms_dict['MasterAggregator-1.00']

            # General plot
            ax = plt.subplot(111)
            #plt.plot(range_time_windows, clusterAlg.plotfmeasure2,'b-', range_time_windows, camnepAlg.plotfmeasure2,'r-', range_time_windows, clusterAlg.plotfmeasure1, 'b--', range_time_windows, camnepAlg.plotfmeasure1, 'r--', range_time_windows, clusterAlg.plotFPR, 'b-.', range_time_windows, camnepAlg.plotFPR, 'r-.', range_time_windows, clusterAlg.plotTPR, 'b:', range_time_windows, camnepAlg.plotTPR, 'r:', range_time_windows, clusterAlg.plotfmeasure05,'g-', range_time_windows, camnepAlg.plotfmeasure05,'c-')
            plt.plot(range_time_windows, clusterAlg.plotfmeasure2,'b-', range_time_windows, clusterAlg.plotfmeasure1, 'b--', range_time_windows, clusterAlg.plotFPR, 'b-.', range_time_windows, clusterAlg.plotTPR, 'b:',  range_time_windows, clusterAlg.plotfmeasure05,'g-')
            plt.legend(('Bclus Fm2', 'CAMNEP Fm2', 'Bclus Fm1', 'CAMNEP Fm1', 'Bclus FPR', 'CAMNEP FPR', 'Bclus TPR', 'CAMNEP TPR', 'Bclus Fm05', 'CAMNEP Fm05'), 'upper center', shadow=True, fancybox=True)
            plt.title('Performance Metrics comparison for '+ str(time_window) + ' seconds.')


        elif comparison_type == 'weight':
            # We only work with bclus and CAMNEP here, we can not plot everything.
            clusterAlg = time_windows_group[-1].algorithms_dict['Bclus']
            #camnepAlg = time_windows_group[-1].algorithms_dict['MasterAggregator-1.00']
            allpositiveAlg = time_windows_group[-1].algorithms_dict['AllPositive']
            # General plot
            ax = plt.subplot(111)
            #plt.plot(range_time_windows, clusterAlg.t_plotfmeasure2,'b-', range_time_windows, camnepAlg.t_plotfmeasure2,'r-', range_time_windows, clusterAlg.t_plotfmeasure1, 'b--', range_time_windows, camnepAlg.t_plotfmeasure1, 'r--', range_time_windows, clusterAlg.t_plotFPR, 'b-.', range_time_windows, camnepAlg.t_plotFPR, 'r-.', range_time_windows, clusterAlg.t_plotTPR, 'b:', range_time_windows, camnepAlg.t_plotTPR, 'r:', range_time_windows, clusterAlg.t_plotfmeasure05,'g-', range_time_windows, camnepAlg.t_plotfmeasure05,'c-')
            ##plt.plot(range_time_windows, clusterAlg.t_plotfmeasure1, 'b--', range_time_windows, camnepAlg.t_plotfmeasure1, 'r--', range_time_windows, clusterAlg.t_plotFPR, 'b-.', range_time_windows, camnepAlg.t_plotFPR, 'r-.', range_time_windows, clusterAlg.t_plotTPR, 'b:', range_time_windows, camnepAlg.t_plotTPR, 'r:')
            plt.plot(range_time_windows, clusterAlg.t_plotfmeasure1, 'b--', range_time_windows, clusterAlg.t_plotFPR, 'b-.', range_time_windows, clusterAlg.t_plotTPR, 'b:' )
            #plt.legend(('Bclus FM1', 'CAMNEP FM1', 'Bclus FPR', 'CAMNEP FPR', 'Bclus TPR', 'CAMNEP TPR'), 'upper center', shadow=True, fancybox=True)
            plt.legend(('Bclus FM1', 'Bclus FPR', 'Bclus TPR'), 'upper center', shadow=True, fancybox=True)
            plt.title('Performance Weighted Metrics comparison for ' + str(time_window) + ' seconds, alpha ' + str(alpha) + '.')

        plt.ylim(ymin=-0.01)
        plt.xlabel('Time window')
        plt.ylabel('%')
        plt.grid(True)

        # ROC plot
        """
        ay = plt.subplot(212)
        plt.plot(clusterAlg.plotFPR, clusterAlg.plotTPR, 'b-', camnepAlg.plotFPR, camnepAlg.plotTPR, 'r-')
        plt.legend(('Cluster', 'CAMNEP'), 'upper center', shadow=True, fancybox=True)
        plt.xlabel('FPR')
        plt.ylabel('TPR')
        plt.title('ROC')
        """
        if plot_file:
            plt.savefig(plot_file, bbox_inches=0, dpi=600)
        else:
            plt.show()


    except Exception as inst:
        if debug:
            print ('Some problem in plot()')
        print (type(inst))     # the exception instance
        print (inst.args)      # arguments stored in .args
        print (inst)           # __str__ allows args to printed directly
        x, y = inst          # __getitem__ allows args to be unpacked directly
        print ('x =', x)
        print ('y =', y)
        exit(-1)





def  extract_columns(line, tw, file_format):
    """
    This function takes a line and extracts the columns. It returns the columns in a dictionary
    """
    try:
        global debug
        global verbose

        #if debug:
            #print (' > Extracting columns')
        
        columns = {} 


        if file_format == 'Netflow':
            # Columns are based on netflow standard
            columns['flow_time'] = line.split()[0]+' '+line.split()[1]

            # Src IP can have a : with the src port or not.
            columns['srcIP'] = line.split()[4]
            if ':' in columns['srcIP']:
                columns['srcIP'] = columns['srcIP'].split(':')[0]

            # Real label
            columns['real_label'] = line.split()[12]
        elif file_format == 'Argus':
            # Columns are based on some argus standard
            columns['flow_time'] = line.split(',')[0]

            # Src IP can have a : with the src port or not.
            columns['srcIP'] = line.split(',')[4]

            # Real label
            columns['real_label'] = line.split(',')[33] #.split('flow=')[1]

        # Store the amount of labels read
        try:
            tw.amount_of_labels[columns['real_label']] += 1
        except KeyError:
            tw.amount_of_labels[columns['real_label']] = 1
        if debug:
            print ('  > Flow time:{0}, srcIP:{1}, Real Label:{2}'.format(columns['flow_time'],columns['srcIP'], columns['real_label']))

        # We shuld read each column based on the algorithm, extract the label and assign it.
        for algorithm_name in tw.algorithms_dict:
            # Predicted label
            try:
                # Normal algorithms
                if file_format == 'Netflow':
                    tw.algorithms_dict[algorithm_name].ip_current_labels[columns['srcIP']] = line.split()[tw.algorithms_dict[algorithm_name].headercolumn].strip('\n')
                elif file_format == 'Argus':
                    tw.algorithms_dict[algorithm_name].ip_current_labels[columns['srcIP']] = line.split(',')[tw.algorithms_dict[algorithm_name].headercolumn].strip('\n')
                if debug:
                    print ('   > Extracting information for algorithm {0}. Label: {1}'.format(algorithm_name,tw.algorithms_dict[algorithm_name].ip_current_labels[columns['srcIP']]))
            except TypeError:
                # Dummy algorithms
                # The header column is being used as predicted label for some dummy algorithm.
                tw.algorithms_dict[algorithm_name].ip_current_labels[columns['srcIP']] = tw.algorithms_dict[algorithm_name].headercolumn
                #if debug:
                    #print ('   > Extracting information for dummy algorithm {0}. Label: {1}'.format(algorithm_name,tw.algorithms_dict[algorithm_name].ip_current_labels[columns['srcIP')]])

        return columns

    except IndexError:
        print ('WARNING! It seems that some columns are missing!')
        exit(-1)

    except Exception as inst:
        if debug:
            print ('Some problem in extract_columns()')
        print (type(inst))     # the exception instance
        print (inst.args)      # arguments stored in .args
        print (inst)           # __str__ allows args to printed directly
        x, y = inst          # __getitem__ allows args to be unpacked directly
        print ('x =', x)
        print ('y =', y)
        exit(-1)


def report_errors(tw):
    """
    This function is used when each time window ends. It takes every algorithm and print (the) errors to the screen. These are live metrics, not the final ones.
    """
    try:
        #global algorithms_dict
        global debug
        global verbose
        global comparison_type

        #B1 is when the predicted label was negative, and the real label was background.
        #print ('B1: Predicted negative, real background.')
        #B2 is when the predicted label was positive, and the real label was background.
        #print ('B2: Predicted positive, real background.')
        #B3 is when the predicted label was background, and the real label was negative.
        #print ('B3: Predicted background, real negative.')
        #B4 is when the predicted label was background, and the real label was positive.
        #print ('B4: Predicted background, real positive.')
        #B5 is when the predicted label was background, and the real label was background.
        #print ('B5: Predicted background, real background.')
        print()

        # Find the longest algo name
        max_name_len = 0
        for i in tw.algorithms_dict:
            if len(i) > max_name_len:
                max_name_len = len(i)

        # Print the time window info
        print (tw)

        # Print the results of each algorithm
        if comparison_type == 'time':
            print ('\n+ Current +')
            for algorithm_name in tw.algorithms_dict:
                tw.algorithms_dict[algorithm_name].current_reportprint(max_name_len)
            print ('\n+ Cumulative +')
            for algorithm_name in tw.algorithms_dict:
                tw.algorithms_dict[algorithm_name].reportprint(max_name_len)
        elif comparison_type == 'weight':
            """
            print ('\n+ Current Normal +')
            for algorithm_name in tw.algorithms_dict:
                tw.algorithms_dict[algorithm_name].current_reportprint(max_name_len)
            """
            print ('\n+ Current Errors +')
            for algorithm_name in tw.algorithms_dict:
                tw.algorithms_dict[algorithm_name].current_reportprint(max_name_len)
            print ('\n+ Current Weighted +')
            for algorithm_name in tw.algorithms_dict:
                tw.algorithms_dict[algorithm_name].weighted_current_reportprint(max_name_len)
            print ('\n+ Cumulative Weighted +')
            for algorithm_name in tw.algorithms_dict:
                tw.algorithms_dict[algorithm_name].weighted_reportprint(max_name_len)
        print()

    except Exception as inst:
        if debug:
            print ('Some problem in report_errors()')
        print (type(inst))     # the exception instance
        print (inst.args)      # arguments stored in .args
        print (inst)           # __str__ allows args to printed directly
        x, y = inst          # __getitem__ allows args to be unpacked directly
        print ('x =', x)
        print ('y =', y)
        exit(-1)


def report_final_errors():
    """
    This function prints for each time window, the final results of each algorithm
    """
    try:
        global debug
        global verbose
        global time_windows_group
        global comparison_type
        global csv_file

        print ('\n\n')
        print ('[+] Final Error Reporting [+]')
        print ('=============================')

        if comparison_type == 'time':
            for algorithm_name in time_windows_group[-1].algorithms_dict:
                time_windows_group[-1].algorithms_dict[algorithm_name].reportprint(30)
            if csv_file:
                csv_handler = open(csv_file, 'a+')
                csv_handler.write('Name,TP,TN,FP,FN,TPR,TNR,FPR,FNR,Precision,Accuracy,ErrorRate,fmeasure1,fmeasure2,fmeasure05,B1,B2,B3,B4,B5\n')
                for algorithm_name in time_windows_group[-1].algorithms_dict:
                    time_windows_group[-1].algorithms_dict[algorithm_name].report_CSV_print(30,csv_handler)
                csv_handler.close()
        elif comparison_type == 'weight':
            print ('\nCumulative Common errors')
            print ('-------------------------')
            for algorithm_name in time_windows_group[-1].algorithms_dict:
                time_windows_group[-1].algorithms_dict[algorithm_name].reportprint(30)
            print ('\nWeighted errors')
            print ('----------------')
            for algorithm_name in time_windows_group[-1].algorithms_dict:
                time_windows_group[-1].algorithms_dict[algorithm_name].weighted_reportprint(30)
            if csv_file:
                csv_handler = open(csv_file, 'a+')
                csv_handler.write('Name,t_TP,t_TN,t_FP,t_FN,t_TPR,t_TNR,t_FPR,t_FNR,t_Precision,t_Accuracy,t_ErrorRate,t_fmeasure1,t_fmeasure2,t_fmeasure05,t_B1,t_B2,t_B3,t_B4,t_B5\n')
                for algorithm_name in time_windows_group[-1].algorithms_dict:
                    time_windows_group[-1].algorithms_dict[algorithm_name].weighted_report_CSV_print(30,csv_handler)
                csv_handler.close()

    except Exception as inst:
        if debug:
            print ('Some problem in report_final_errors()')
        print (type(inst))     # the exception instance
        print (inst.args)      # arguments stored in .args
        print (inst)           # __str__ allows args to printed directly
        x, y = inst          # __getitem__ allows args to be unpacked directly
        print ('x =', x)
        print ('y =', y)
        exit(-1)



def generate_algorithms(headersline, tw, file_format):
    """ Generate all the algorithms objects. One for each column in the file """
    try:
        global debug
        global verbose
        #global algorithms_dict

        temp_real_negative_label = ''
        temp_real_positive_label = ''
        temp_real_background_label = ''

        if debug:
            print (' > Headers line read: {0}'.format(headersline))

        # Find algorithms names and number by reading the first line.
        if file_format == 'Netflow':
            split_headers = headersline.split()[12:]
        if file_format == 'Argus':
            split_headers = headersline.split(',')[34:]
        
        for algorithm_header in split_headers:
            if debug:
                print ('  >> Algorithm header read: {0}'.format(algorithm_header))
            algorithm_name = algorithm_header.split('(')[0]
            if file_format == 'Netflow':
                algorithm_headercolumn = split_headers.index(algorithm_header) + 12
            elif file_format == 'Argus':
                algorithm_headercolumn = split_headers.index(algorithm_header) + 34
            try:
                algorithm_negative_label = algorithm_header.split('(')[1].split(')')[0].split(':')[0]
                algorithm_positive_label = algorithm_header.split('(')[1].split(')')[0].split(':')[1]
            except IndexError:
                # This column is not a column with labels because it does not have the ()
                continue

            try:
                algorithm_background_label = algorithm_header.split('(')[1].split(')')[0].split(':')[2]
            except IndexError:
                # There is no background label for this algorithm
                algorithm_background_label = ''

            if debug:
                print ('    > Algorithm name: {0} (column {3}). Positive label: {1}, Negative Label: {2}, Background Label: {4}'.format(algorithm_name, algorithm_positive_label, algorithm_negative_label, algorithm_headercolumn, algorithm_background_label))

            temp_real_positive_label = algorithm_positive_label
            temp_real_negative_label = algorithm_negative_label
            temp_real_background_label = algorithm_background_label

            # Create the algorithm object
            temp_algorithm = algorithm()
            temp_algorithm.name = algorithm_name
            temp_algorithm.headercolumn = algorithm_headercolumn
            # Negative predicted label
            temp_algorithm.algorithm_labels[0] = algorithm_negative_label
            # Positive predicted label
            temp_algorithm.algorithm_labels[1] = algorithm_positive_label
            # Background predicted label
            temp_algorithm.algorithm_labels[2] = algorithm_background_label
            # Real negative label
            temp_algorithm.real_labels[0] = temp_real_negative_label
            # Real positive label
            temp_algorithm.real_labels[1] = temp_real_positive_label
            # Real background label
            temp_algorithm.real_labels[2] = temp_real_background_label

            # Store it in the global dict
            newalgorithm = temp_algorithm
            print(newalgorithm.algorithm_labels)
            tw.algorithms_dict[newalgorithm.name] = newalgorithm

        # End for


        # Create the dummy algorithm that predicts everything as a Botnet
        temp_algorithm = algorithm()
        temp_algorithm.name = 'AllPositive'
        # For these dummy algorithms, the headercolumn is used as predicted label. Because they do not exist in the netflow overall table.
        temp_algorithm.headercolumn = temp_real_positive_label
        # Negative predicted label
        temp_algorithm.algorithm_labels[0] = 'Not Defined'
        # Positive predicted label
        temp_algorithm.algorithm_labels[1] = temp_real_positive_label
        # Background predicted label
        temp_algorithm.algorithm_labels[2] = 'Not Defined'
        # Real negative label
        temp_algorithm.real_labels[0] = temp_real_negative_label
        # Real positive label
        temp_algorithm.real_labels[1] = temp_real_positive_label
        # Real background label
        temp_algorithm.real_labels[2] = temp_real_background_label
        # Store it in the global dict
        newalgorithm = temp_algorithm
        tw.algorithms_dict[newalgorithm.name] = newalgorithm


        # Create the dummy algorithm that predicts everything as Normal
        temp_algorithm = algorithm()
        temp_algorithm.name = 'AllNegative'
        # For these dummy algorithms, the headercolumn is used as predicted label. Because they do not exist in the netflow overall table.
        temp_algorithm.headercolumn = temp_real_negative_label
        # Negative predicted label
        temp_algorithm.algorithm_labels[0] = temp_real_negative_label
        # Positive predicted label
        temp_algorithm.algorithm_labels[1] = 'Not Defined'
        # Background predicted label
        temp_algorithm.algorithm_labels[2] = 'Not Defined'
        # Real negative label
        temp_algorithm.real_labels[0] = temp_real_negative_label
        # Real positive label
        temp_algorithm.real_labels[1] = temp_real_positive_label
        # Real background label
        temp_algorithm.real_labels[2] = temp_real_background_label
        # Store it in the global dict
        newalgorithm = temp_algorithm
        tw.algorithms_dict[newalgorithm.name] = newalgorithm

        # Create the dummy algorithm that predicts everything as Background
        temp_algorithm = algorithm()
        temp_algorithm.name = 'AllBackground'
        # For these dummy algorithms, the headercolumn is used as predicted label. Because they do not exist in the netflow overall table.
        temp_algorithm.headercolumn = temp_real_background_label
        # Negative predicted label
        temp_algorithm.algorithm_labels[0] = 'Not Defined'
        # Positive predicted label
        temp_algorithm.algorithm_labels[1] = 'Not Defined'
        # Background predicted label
        temp_algorithm.algorithm_labels[2] = temp_real_background_label
        # Real negative label
        temp_algorithm.real_labels[0] = temp_real_negative_label
        # Real positive label
        temp_algorithm.real_labels[1] = temp_real_positive_label
        # Real background label
        temp_algorithm.real_labels[2] = temp_real_background_label
        # Store it in the global dict
        newalgorithm = temp_algorithm
        tw.algorithms_dict[newalgorithm.name] = newalgorithm

        if debug:
            print ('End generating the algorithms...\n')

    except Exception as inst:
        if debug:
            print ('Some problem in generate_algorithms')
        print( type(inst))     # the exception instance
        print (inst.args)      # arguments stored in .args
        print (inst)           # __str__ allows args to printed directly
        x, y = inst          # __getitem__ allows args to be unpacked directly
        print ('x =', x)
        print ('y =', y)
        exit(-1)


def process_file(file, comparison_type, time_window): 
    """
    This function takes a file, time window and comparison type and generates the staditistics of the detection performance of every algorithm. Type can be 'flow' based or 'time' based. 
    """
    try:
        global debug
        global verbose
        global time_window_id
        global time_windows

        processing_init_time = datetime.now()

        if debug:
            print ('Processsing file...')

        # Open the file for reading
        #f = open(file,'r')

        # Read the first line. The headers line...
        line = file.readline()

        if line[0] != '#':
            print()
            print ('WARNING! The first line must be commented with #, and be the headers line!!!')
            print()
            exit(-1)


        # Find out if the columns are space separated or comma separated
        if len(line.split()) > len(line.split(',')):
            # Space separated. This means the old netflow format
            file_format = 'Netflow'
            if debug:
                print ('Netflow file format. Space separated')
        else:
            # Comma separated. This means the new biargus format
            file_format = 'Argus'
            if debug:
                print ('Argus file format. Comma separated')

        # Create an empty time window. For the flow-by-flow analysis this is the only time window. For the time-based analysis it is the first
        tw = time_windows()

        # Clean the algorithms ip labels
        tw.clean_ip_labels()

        # Generate the algorithms objects and identify the columns
        generate_algorithms(line, tw, file_format)

        # Read the second line. 
        line = f.readline()

        # If comparison is flow based...
        if comparison_type == 'flow':
            if debug:
                print ('Comparing labels flow by flow...')
                print ('Using file {0}.'.format(file))

            # We already read two lines
            tw.lines_read = 1

            while (line):
                # No comments
                if line[0] == '#':
                    try:
                        line = f.readline()
                        while (line[0]=='#'):
                            line = f.readline()
                    except IndexError:
                        # The file can end with comments
                        continue

                #if debug:
                    #print ('>-------------\n> Reading line:{0}'.format(line))


                # Extract the columns correctly
                columns = extract_columns(line,tw, file_format)

                # Compute the error with the predicted label and the real label
                for algorithm_name in tw.algorithms_dict:
                    try:
                        predicted_label = tw.algorithms_dict[algorithm_name].ip_current_labels[columns['srcIP']]
                        tw.algorithms_dict[algorithm_name].compute_error(predicted_label, columns['real_label'])

                    except KeyError:
                        # The algorithm does not have any predicted label.
                        continue

                # Read next line
                line = f.readline()
                tw.lines_read = tw.lines_read + 1


            # Last line is empty
            tw.lines_read = tw.lines_read - 1

            # Verify the amount of labels.
            total = 0
            for label in tw.amount_of_labels:
                total = total + tw.amount_of_labels[label]
            if tw.lines_read != total:
                print()
                print ('WARNING! The amount of labels read is not the same that the amount of labels in the file.')
                print ('Lines read: {0}'.format(tw.lines_read))
                for label in tw.amount_of_labels:
                    print ('Amount of {0} labels: {1}'.format(label, tw.amount_of_labels[label]))
                print ('Total amount of labels: {0}'.format(total))
                exit(-1)

            # Report errors
            report_errors(tw)



        # If comparison is time based or weight based...
        elif comparison_type == 'time' or comparison_type == 'weight':
            if debug:
                print ('\nComparing labels flows using a ' + str(time_window) + ' seconds time window.')
                print ('Using file {0}.'.format(file))

            # Store the time windows in the vector
            time_windows_group.append(tw)

            # Link the algorithms dict with the time window, so we can access the info from the tw
            #tw.algorithms_dict = algorithms_dict


            # No comments
            if line[0] == '#':
                line = f.readline()
                while (line[0]=='#'):
                    line = f.readline()

            # Get the start time
            # our flows times are like this: 2011-08-16 10:30:00.081
            if file_format == 'Netflow':
                time_window_flow_start_time = datetime.strptime(line.split()[0]+' '+line.split()[1], "%Y-%m-%d %H:%M:%S.%f")
            elif file_format == 'Argus':
                time_window_flow_start_time = datetime.strptime(line.split(',')[0], "%Y/%m/%d %H:%M:%S.%f")

            while (line):

                # Do not read comments
                if line[0] == '#':
                    line = f.readline()
                    continue

                # Current time
                if file_format == 'Netflow':
                    current_flow_start_time =  datetime.strptime(line.split()[0]+' '+line.split()[1], "%Y-%m-%d %H:%M:%S.%f")
                elif file_format == 'Argus':
                    current_flow_start_time =  datetime.strptime(line.split(',')[0], "%Y/%m/%d %H:%M:%S.%f")

                # Compute the difference
                delta_time = current_flow_start_time - time_window_flow_start_time
                    #print (' > Current labels: original= {0}. srcIP={1}. Algorithms: {2}'.format(columns['real_label'], columns['srcIP'], tw.algorithms_labels_for_this_ip(columns['srcIP')]) )

                # Differentiate between the time windows. Only < and not <=.
                if delta_time.total_seconds() < time_window:
                    # We are inside the specified time window
                    #if debug:
                        #print ('> -------------\n> Reading line in this time window: {0}'.format(line.strip()))
                        #print (' > Delta time: {0} (time window={1})'.format(delta_time.total_seconds(),time_window))
                        #print (' Inside the current time windows.')


                    # Extract the columns correctly
                    columns = extract_columns(line, tw, file_format)

                    tw.lines_read = tw.lines_read + 1


                    # Add the label for the current ip. Check uniqueness.
                    tw.add_ip_label(columns['srcIP'], columns['real_label'])

                    # Read next line. This should be inside this if, and not outside. Otherwise we lose the last line read.
                    line = f.readline()

                else:
                    # We are outside the time window

                    #if debug:
                    #    print ('> -------------\n> Reading line outside this time window: {0}'.format(line))
                    #print (' > Delta time: {0} (time window={1})'.format(delta_time.total_seconds(),time_window))

                    if debug:
                        print (' > Analyzing the time window {0}'.format(tw.id))

                    # We should compute errors for EACH IP address seen...
                    tw.compute_errors()

                       
                    ###############################################
                    # If in weighted mode, compute the weight errors
                    if comparison_type == 'weight':
                        tw.compute_weighted_errors()
                    ###############################################

                    #print ('\nAmount of ips in the time window number {1}: {0}'.format(tw.amount_of_ips, tw.id))
                    report_errors(tw)

                    # Update the ploting values for each algorithm. This way we have one value each time the time windows ends.
                    ###############################################
                    # If in weighted mode, compute the weight errors
                    if comparison_type == 'weight':
                        for alg in tw.algorithms_dict:
                            tw.algorithms_dict[alg].update_weighted_plot()
                    elif comparison_type == 'time':
                        for alg in tw.algorithms_dict:
                            tw.algorithms_dict[alg].updateplot()
                    ###############################################

                    # New time window start time
                    if file_format == 'Netflow':
                        time_window_flow_start_time = datetime.strptime(line.split()[0]+' '+line.split()[1], "%Y-%m-%d %H:%M:%S.%f")
                    elif file_format == 'Argus':
                        time_window_flow_start_time = datetime.strptime(line.split(',')[0], "%Y/%m/%d %H:%M:%S.%f")

                    # Store the algorithms names for the next time window
                    temp_algorithms = tw.algorithms_dict

                    # Create the next time window object
                    tw = time_windows()
    
                    # Copy the algorithms to the next time window
                    tw.algorithms_dict = temp_algorithms

                    # We should empty the dictionaries
                    tw.clean_ip_labels()

                    # Store the time windows in the vector
                    time_windows_group.append(tw)

            # Here we are out of the while

            # Check if there are still IPs that were not analyzed. 
            # It is the case when the file ends during the time window and we did not process the last lines of the last time window.
            # In short, we did not go into the 'the time windows ended' part.

            if tw.ip_original_labels:
                if debug:
                    print ('> There were still some lines not processed because the file ended but not the time window.')
                # The las line belongs to this time window
                tw.lines_read = tw.lines_read + 1

                # There is still something in the dictionary! process it.
                tw.compute_errors()

                #if verbose:
                    #print ('\nAmount of ips in the time window number {1}: {0}'.format(tw.amount_of_ips, tw.id))
                    #report_errors(tw)

                ###############################################
                # If in weighted mode, compute the weight errors
                if comparison_type == 'weight':
                    tw.compute_weighted_errors()
                ###############################################

                # Update the ploting values for each algorithm. This way we have one value each time the time windows ends.
                ###############################################
                # If in weighted mode, compute the weight errors
                if comparison_type == 'weight':
                    for alg in tw.algorithms_dict:
                        tw.algorithms_dict[alg].update_weighted_plot()
                elif comparison_type == 'time':
                    for alg in tw.algorithms_dict:
                        tw.algorithms_dict[alg].updateplot()
                ###############################################


            # Last line is empty
            tw.lines_read = tw.lines_read - 1

            #print()
            #print ('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            #print()
            #print ('Lines read: {0}'.format(tw.lines_read))
            #print ('Amount of normal labels: {0}'.format(tw.amount_of_labels))
            #print ('Amount of time windows: {0}\n'.format(tw.id))
            #print ('Time window width: {0}\n'.format(time_window))

            # Report errors
            report_errors(tw)
       

        # After the ifs, we now have to compute the final metrics
        report_final_errors()


        # Processing time computing
        processing_finish_time = datetime.now()
        delta = processing_finish_time - processing_init_time
        print ('\nProcessing lasted {0} seconds'.format(delta.seconds))



    except Exception as inst:
        if debug:
            print ('Some problem in process_file()')
        print (type(inst))     # the exception instance
        print (inst.args)      # arguments stored in .args
        print (inst)           # __str__ allows args to printed directly
        x, y = inst          # __getitem__ allows args to be unpacked directly
        print ('x =', x)
        print ('y =', y)
        exit(-1)