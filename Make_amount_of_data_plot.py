import os
import glob
import numpy as np
import sys
import Make_comparison_plots_v6 as mcp
import pdb



# Step 0 : Define constants

# Step 0.1 : Define directories

MIN_NBR_YRS_DIRECTORY         = '/num-years1'
NUMPY_DIRECTORY               = '/npy'
PNG_DIRECTORY                 = '/png'
SAMPLING_PERCENTAGE_DIRECTORY = '/sampling-percentage'
SNOW_COMEAU_DIRECTORY         = '/snow/comeau/FLUXNET_America/AMF_1990-2017'
#SNOW_DILUCA_DIRECTORY         = '/snow/diluca/FLUXNET_America/1990-2017/v1/TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE'
SNOW_DILUCA_DIRECTORY         = '/snow/diluca/FLUXNET_America/1990-2017/v2/TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE'


# Step 0.2 : Define filenames

STATION_NAMES_FILENAME = 'AMF_station-filelist_1990-2017_TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE.txt'
SUMMARY_FILENAME       = 'AMF_summary_1990-2017_TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE.txt'


# Step 0.3 : Define prefixes and suffixes

PNG_SUFFIX = '.png'


# Step 0.4 : Define delimiters

STATION_NAMES_DELIMITER        = '_'
STATION_NBRS_AND_IDS_DELIMITER = ' '
NBR_OF_YRS_OF_DATA_DELIMITER   = ' '


# Step 0.5 : Define special characters

NEW_LINE_CHAR = '\n'
NULL_CHAR     = ''
READING_CHAR  = 'r'
SLASH_BAR     = '/'
STAR          = '*'


# Step 0.6 : Define indexes

DATE_INDEX               = 0
FILEPATH_INDEX           = 0
NBR_OF_YRS_OF_DATA_INDEX = 4
STATION_ID_INDEX         = 3
STATION_NBR_INDEX        = 2


# Step 0.7 : Define values

DATA_ID              = 'data'
DATES_ID             = 'dates'
MIN_NBR_DATA         = ['1', '2', '4', '5', '6']
NBR_OF_HEADER_ROWS   = 3
SAMPLING_PERCENTAGES = ['10', '25', '50', '75', '90']  # minimum sampling percentages
STATION_TO_SKIP      = 'US-Ro1'                        # station is only present when sampling percentage is 90%, rendering comparisons impossible


# Step 0.7 : Define plot constants

NBR_OF_ENTRY_RATIOS_Y_AXIS_LABEL = 'nbr of entries ratio (30 mins / 180 mins)'
NBR_OF_YRS_OF_DATA_Y_AXIS_LABEL  = 'nbr of years of data (180 mins avg)'

NBR_OF_ENTRY_RATIOS_AND_YRS_OF_DATA_LEGEND_LABEL_1 = 'AMF - ('
NBR_OF_ENTRY_RATIOS_AND_YRS_OF_DATA_LEGEND_LABEL_2 = '/6+ data)'

'''
NBR_OF_ENTRIES_CAPTION      = Number of entries of available AmeriFlux (AMF) data according to AMF station. Stations are referred to by their id number, country (Canada or United States) and station name.
a) Number of entries of available data. Blue bars represent data averaged over 30 minutes. Orange bars represent data averaged over 180 minutes, ie the resampled results.
Resampling involved two criteria : 1) A minimum number of years of data must be available at the station; 2) 180 minutes average is calculated only if more than a certain
percentage of the corresponding 30 minutes data is present. b) Relative difference in the number of entries of available data for the 180 minutes average compared to the
30 minutes average.
'''

PLOT_TYPE = 'nbr-of-entries-ratio-and-yrs'

nbr_of_entry_ratios_all_stations = []
nbr_of_yrs_of_data_all_stations  = []

nbr_of_entry_ratios_and_yrs_of_data_legend_labels_all = []
station_ids_all_sampling_percentages = []

for sampling_percentage in SAMPLING_PERCENTAGES :

    station_to_skip_nbr = 0  # station number of the station to skip

    # Step 1 : Obtain station numbers, ids and station filepaths

    station_names_file_pathname = SNOW_DILUCA_DIRECTORY + SAMPLING_PERCENTAGE_DIRECTORY + sampling_percentage + MIN_NBR_YRS_DIRECTORY + SLASH_BAR + STATION_NAMES_FILENAME
    station_names_file          = open(station_names_file_pathname, READING_CHAR)

    station_nbrs_list         = []
    station_ids_list          = [] 
    dates_3_hr_filepaths_list = []

    for station_names_line in station_names_file :

        amf_filename        = os.path.basename(station_names_line)
        station_nbr         = amf_filename.split(STATION_NAMES_DELIMITER)[STATION_NBR_INDEX]
        station_id          = amf_filename.split(STATION_NAMES_DELIMITER)[STATION_ID_INDEX]
        dates_3_hr_filepath = station_names_line.replace(NEW_LINE_CHAR, NULL_CHAR).replace(SLASH_BAR+SLASH_BAR, SLASH_BAR).replace(DATA_ID, DATES_ID)

        if ( station_id != STATION_TO_SKIP ) :

            station_ids_list.append(station_id)
            station_nbrs_list.append(station_nbr)
            dates_3_hr_filepaths_list.append(dates_3_hr_filepath)

        else :

            station_to_skip_nbr = int(station_nbr)

    station_names_file.close()
    #station_ids_list.sort()
    station_ids_all_sampling_percentages.append(station_ids_list)
    #pdb.set_trace()


    # Step 2 : Obtain ratios of number of entries (0.5 over 3 hour averages)

    nbr_of_entries_ratios_per_station = []

    for dates_3_hr_filepath, station_id in zip(dates_3_hr_filepaths_list, station_ids_list) :

        dates_3_hr          = np.load(dates_3_hr_filepath)
        nbr_of_entries_3_hr = dates_3_hr.shape[DATE_INDEX]

        dates_0_5_hr_filepath_pattern = SNOW_COMEAU_DIRECTORY + NUMPY_DIRECTORY + SLASH_BAR + STAR + DATES_ID + STAR + station_id + STAR
        dates_0_5_hr_filepath         = glob.glob(dates_0_5_hr_filepath_pattern)[FILEPATH_INDEX]
        dates_0_5_hr                  = np.load(dates_0_5_hr_filepath)
        nbr_of_entries_0_5_hr         = dates_0_5_hr.shape[DATE_INDEX]

        nbr_of_entries_ratio = round( (nbr_of_entries_0_5_hr / nbr_of_entries_3_hr), 3)

        nbr_of_entries_ratios_per_station.append(nbr_of_entries_ratio)
        #pdb.set_trace()


	
    # Step 3 : Obtain number of years of data for 3 hour averages

    nbr_of_yrs_of_data_filename = SUMMARY_FILENAME
    nbr_of_yrs_of_data_pathname = SNOW_DILUCA_DIRECTORY + SAMPLING_PERCENTAGE_DIRECTORY + sampling_percentage + MIN_NBR_YRS_DIRECTORY + SLASH_BAR + nbr_of_yrs_of_data_filename

    nbr_of_yrs_of_data_per_station = []

    nbr_of_yrs_of_data_file = open(nbr_of_yrs_of_data_pathname, READING_CHAR)

    nbr_of_yrs_of_data_line_counter = 1
    nbr_of_stations                 = len(station_nbrs_list)

    for nbr_of_yrs_of_data_line in nbr_of_yrs_of_data_file :

        if ( ( nbr_of_yrs_of_data_line_counter > NBR_OF_HEADER_ROWS ) and ( nbr_of_yrs_of_data_line_counter < ( nbr_of_stations + NBR_OF_HEADER_ROWS + 1 ) ) ) :

            station_nbr = int( nbr_of_yrs_of_data_line.split(NBR_OF_YRS_OF_DATA_DELIMITER)[3].replace(':', '') )

            if ( station_nbr != station_to_skip_nbr ) :
 
                nbr_of_yrs_of_data = float( nbr_of_yrs_of_data_line.split(NBR_OF_YRS_OF_DATA_DELIMITER)[NBR_OF_YRS_OF_DATA_INDEX].replace(NEW_LINE_CHAR, NULL_CHAR) )
                nbr_of_yrs_of_data_per_station.append(nbr_of_yrs_of_data)
                #pdb.set_trace()

            else :
                nbr_of_yrs_of_data_line_counter = nbr_of_yrs_of_data_line_counter - 1

        nbr_of_yrs_of_data_line_counter = nbr_of_yrs_of_data_line_counter + 1

    nbr_of_yrs_of_data_file.close()

    nbr_of_entry_ratios_all_stations.append(nbr_of_entries_ratios_per_station)
    nbr_of_yrs_of_data_all_stations.append(nbr_of_yrs_of_data_per_station)
 
    min_nbr_of_data                                  = MIN_NBR_DATA[ SAMPLING_PERCENTAGES.index(sampling_percentage) ]
    nbr_of_entry_ratios_and_yrs_of_data_legend_label = NBR_OF_ENTRY_RATIOS_AND_YRS_OF_DATA_LEGEND_LABEL_1 + min_nbr_of_data + NBR_OF_ENTRY_RATIOS_AND_YRS_OF_DATA_LEGEND_LABEL_2 
    nbr_of_entry_ratios_and_yrs_of_data_legend_labels_all.append(nbr_of_entry_ratios_and_yrs_of_data_legend_label)
    #pdb.set_trace()


# Step 4 : Produce plot of ratios and number of years of data
     
station_nbrs_and_ids = []

for station_nbr, station_id in zip( station_nbrs_list, station_ids_list ) :

    station_nbr_and_id = station_nbr + STATION_NBRS_AND_IDS_DELIMITER + station_id

    station_nbrs_and_ids.append(station_nbr_and_id)

plot_filename = PLOT_TYPE + MIN_NBR_YRS_DIRECTORY.replace(SLASH_BAR, STATION_NAMES_DELIMITER) + PNG_SUFFIX
plot_pathname = SNOW_COMEAU_DIRECTORY + PNG_DIRECTORY + SLASH_BAR + plot_filename

#pdb.set_trace()

mcp.Make_comparison_plot(station_nbrs_and_ids, nbr_of_entry_ratios_all_stations, nbr_of_yrs_of_data_all_stations, NBR_OF_ENTRY_RATIOS_Y_AXIS_LABEL, NBR_OF_YRS_OF_DATA_Y_AXIS_LABEL, nbr_of_entry_ratios_and_yrs_of_data_legend_labels_all, nbr_of_entry_ratios_and_yrs_of_data_legend_labels_all, plot_pathname)
