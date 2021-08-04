import os
import glob
import fluxnet_classes as fc
import numpy as np
import Make_comparison_plots_v4 as mcp
import pdb



# Step 0 : Define constants

FILTERED_DATA_COMMON_DIRECTORY               = '/snow/diluca/FLUXNET_America/1990-2021/v1/TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE'
FILTERED_DATA_SAMPLING_PERCENTAGES_DIRECTORY = 'sampling-percentage'
FILTERED_DATA_MIN_NBR_YRS_DIRECTORY          = 'num-years'

SAMPLING_PERCENTAGES = ['25', '50', '75']  # minimum sampling percentages
MIN_NBR_YRS          = ['1', '2', '5']     # minimum number of years of available data

FILTERED_DATA_FILENAME  = 'AMF_summary_1990-2021_TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE.txt'
STATION_NAMES_FILENAME  = 'AMF_station-filelist_1990-2021_TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE.txt'

DELIMITER_STATION_NAMES = '_'

NBR_OF_HEADER_ROWS_FILTERED_DATA = 3
DELIMITER_FILTERED_DATA          = ' '
NEW_LINE_CHAR                    = '\n'
NULL_CHAR                        = ''

UNFILTERED_DATA_DIRECTORY          = '/home/data/Validation/AmeriFlux'
NBR_OF_HEADER_ROWS_UNFILTERED_DATA = 3
UNFILTERED_DATA_SUMMARY_DIRECTORY  = '/snow/comeau/FLUXNET_America/AMF_1990-2019'

Y_AXIS_LABEL            = 'Nbr of years available'
LABEL_PRE_PROCESSING    = 'AMF -  30 mins'
LABEL_POST_PROCESSING_1 = 'AMF - 180 mins ('
LABEL_POST_PROCESSING_2 = ' yr(s), '
LABEL_POST_PROCESSING_3 = '%)' 
CAPTION                 = '''Number of years of available AmeriFlux (AMF) data according to AMF station. Stations are referred to by their id number, country (Canada or United States) and station name.
a) Number of years of available data. Blue bars represent data averaged over 30 minutes, corresponding to pre-processed data. Orange bars represent data averaged over
180 minutes, ie the post-processing results. Processing involved two criteria : 1) A minimum number of years of data must be available at the station; 2) 180 minutes average is
calculated only if more than a certain percentage of the corresponding 30 minutes data is present. b) Relative difference in the number of years of available data compared to 
pre-processing values. A small relative difference indicates a small loss of data.'''



# Step 1 : Obtain number of years ploting function parameters

for sampling_percentage in SAMPLING_PERCENTAGES :

    for min_nbr_yrs in MIN_NBR_YRS :

        # Step 1.1 : Obtain station numbers and ids

        station_names_pathname = FILTERED_DATA_COMMON_DIRECTORY + '/' + FILTERED_DATA_SAMPLING_PERCENTAGES_DIRECTORY + sampling_percentage + '/' + FILTERED_DATA_MIN_NBR_YRS_DIRECTORY + min_nbr_yrs + '/' + STATION_NAMES_FILENAME
        file_station_names     = open(station_names_pathname, 'r')
        #pdb.set_trace()

        station_nbrs_list = []
        station_ids_list  = []

        for line_station_names in file_station_names :

            amf_filename = os.path.basename(line_station_names)
            station_nbr  = int(amf_filename.split(DELIMITER_STATION_NAMES)[2])
            station_id   = amf_filename.split(DELIMITER_STATION_NAMES)[3]

            station_nbrs_list.append(station_nbr)
            station_ids_list.append(station_id)
            #pdb.set_trace()

        file_station_names.close()
        #pdb.set_trace()


        # Step 1.2 : Obtain variable names

        unfiltered_data_summary_pathname = UNFILTERED_DATA_SUMMARY_DIRECTORY + '/' + FILTERED_DATA_FILENAME

        var_names      = FILTERED_DATA_FILENAME.split('_', 3)[3].replace('.txt', NULL_CHAR)
        var_names_list = var_names.split('-')
        #pdb.set_trace()



        # Step 1.3 : Obtain number of years available for filtered data

        filtered_data_pathname = FILTERED_DATA_COMMON_DIRECTORY + '/' + FILTERED_DATA_SAMPLING_PERCENTAGES_DIRECTORY + sampling_percentage + '/' + FILTERED_DATA_MIN_NBR_YRS_DIRECTORY + min_nbr_yrs + '/' + FILTERED_DATA_FILENAME
        file_filtered_data     = open(filtered_data_pathname, 'r')
        #pdb.set_trace()

        for line_nbr in range(0, NBR_OF_HEADER_ROWS_FILTERED_DATA) :
            file_filtered_data.readline()

        nbr_of_yrs_filtered_data_list = []  # represents data_2 entry

        for line_filtered_data in file_filtered_data :

            nbr_of_yrs = float(line_filtered_data.split(DELIMITER_FILTERED_DATA)[4].replace(NEW_LINE_CHAR, NULL_CHAR))

            nbr_of_yrs_filtered_data_list.append(nbr_of_yrs)
            #pdb.set_trace()

        file_filtered_data.close()
        nbr_of_yrs_filtered_data_list.pop( len(nbr_of_yrs_filtered_data_list) - 1 )
        #pdb.set_trace()


        # Step 1.4 : Obtain number of years available for unfiltered data

        # Step 1.4.1 : Obtain summary function parameters

        total_unfiltered_data_list = []

        for station_id in station_ids_list :

            unfiltered_data_pathname_pattern = UNFILTERED_DATA_DIRECTORY + '/' + 'AMF_' + station_id + '*' + '.csv'
            unfiltered_data_pathname         = glob.glob(unfiltered_data_pathname_pattern)[0]
            file_unfiltered_data             = open(unfiltered_data_pathname, 'r')

            for line_nbr in range(0, NBR_OF_HEADER_ROWS_UNFILTERED_DATA - 1) :
                file_unfiltered_data.readline()

            var_names_unfiltered_data = file_unfiltered_data.readline().split(',')
            #pdb.set_trace()

            unfiltered_data_list = []

            for line_unfiltered_data in file_unfiltered_data :
                unfiltered_data_list.append(line_unfiltered_data)
                #pdb.set_trace()

            total_unfiltered_data_list.append(len(unfiltered_data_list))
            #pdb.set_trace()
    
        t_freq = [0.5] * len(total_unfiltered_data_list)


        # Step 1.4.2 : Create summary file for unfiltered data

        fc.print_summary(total_unfiltered_data_list, unfiltered_data_summary_pathname, t_freq, var_names) 
        #pdb.set_trace()


        # Step 1.4.3 : Read summary file for unfiltered data

        unfiltered_data_pathname = unfiltered_data_summary_pathname
        file_unfiltered_data     = open(unfiltered_data_pathname, 'r')

        for line_nbr in range(0, NBR_OF_HEADER_ROWS_FILTERED_DATA) :
            file_unfiltered_data.readline()

        nbr_of_yrs_unfiltered_data_list = []  # represents data_2 entry

        for line_unfiltered_data in file_unfiltered_data :

            nbr_of_yrs = float(line_unfiltered_data.split(DELIMITER_FILTERED_DATA)[4].replace(NEW_LINE_CHAR, NULL_CHAR))

            nbr_of_yrs_unfiltered_data_list.append(nbr_of_yrs)
            #pdb.set_trace()

        file_unfiltered_data.close()
        nbr_of_yrs_unfiltered_data_list.pop( len(nbr_of_yrs_unfiltered_data_list) - 1 )
        #pdb.set_trace()



        # Step 2 : Create plots

        label_post_processing = LABEL_POST_PROCESSING_1 + min_nbr_yrs + LABEL_POST_PROCESSING_2 + sampling_percentage + LABEL_POST_PROCESSING_3
        station_numbers       = np.array(station_nbrs_list)
        station_names         = np.array(station_ids_list)
        data_1                = np.array(nbr_of_yrs_unfiltered_data_list)
        data_2                = np.array(nbr_of_yrs_filtered_data_list)

        plot_filename = 'nbr-of-years-of-data_' + FILTERED_DATA_SAMPLING_PERCENTAGES_DIRECTORY + sampling_percentage + '_' + FILTERED_DATA_MIN_NBR_YRS_DIRECTORY + min_nbr_yrs + '.png'
        plot_pathname = UNFILTERED_DATA_SUMMARY_DIRECTORY + '/' + 'png' + '/' + plot_filename

        mcp.Make_comparison_plot(station_numbers, station_names, data_1, data_2, Y_AXIS_LABEL, LABEL_PRE_PROCESSING, label_post_processing, CAPTION, plot_pathname)
        #pdb.set_trace()


        """
        # Step 3 : Obtain average values ploting function parameters

        var_names_list = var_names.split('-')

        time_length_list = [ 365 * 24 ] * len(total_unfiltered_data_list)

        #pdb.set_trace()
        """
