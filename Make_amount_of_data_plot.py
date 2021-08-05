import os
import glob
import numpy as np
import Make_comparison_plots_v4 as mcp
import pdb



# Step 0 : Define constants

# Step 0.1 : Define directories

MIN_NBR_YRS_DIRECTORY         = '/num-years'
NUMPY_DIRECTORY               = '/npy'
PNG_DIRECTORY                 = '/png'
SAMPLING_PERCENTAGE_DIRECTORY = '/sampling-percentage'
SNOW_COMEAU_DIRECTORY         = '/snow/comeau/FLUXNET_America/AMF_1990-2019'
SNOW_DILUCA_DIRECTORY         = '/snow/diluca/FLUXNET_America/1990-2021/v1/TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE'


# Step 0.2 : Define filenames

STATION_NAMES_FILENAME = 'AMF_station-filelist_1990-2021_TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE.txt'


# Step 0.3 : Define prefixes and suffixes

PNG_SUFFIX = '.png'


# Step 0.3 : Define delimiters

STATION_NAMES_DELIMITER = '_'


# Step 0.4 : Define special characters

NEW_LINE_CHAR = '\n'
NULL_CHAR     = ''
READING_CHAR  = 'r'
SLASH_BAR     = '/'
STAR          = '*'


# Step 0.5 : Define indexes

DATE_INDEX        = 0
FILEPATH_INDEX    = 0
STATION_ID_INDEX  = 3
STATION_NBR_INDEX = 2


# Step 0.6 : Define values

DATA_ID              = 'data'
DATES_ID             = 'dates'
MIN_NBR_YRS          = ['1', '2', '5']     # minimum number of years of available data
SAMPLING_PERCENTAGES = ['25', '50', '75']  # minimum sampling percentages
MIN_NBR_DATA         = ['2', '4', '5']


# Step 0.7 : Define plot constants

NBR_OF_ENTRIES_Y_AXIS_LABEL = 'Nbr of entries available'
NBR_OF_ENTRIES_0_5_HR_LABEL = 'AMF -  30 mins'
NBR_OF_ENTRIES_3_HR_LABEL_1 = 'AMF - 180 mins ('
NBR_OF_ENTRIES_3_HR_LABEL_2 = ' yr(s), '
NBR_OF_ENTRIES_3_HR_LABEL_3 = '/6+ data)'

'''
NBR_OF_ENTRIES_CAPTION      = Number of entries of available AmeriFlux (AMF) data according to AMF station. Stations are referred to by their id number, country (Canada or United States) and station name.
a) Number of entries of available data. Blue bars represent data averaged over 30 minutes. Orange bars represent data averaged over 180 minutes, ie the resampled results.
Resampling involved two criteria : 1) A minimum number of years of data must be available at the station; 2) 180 minutes average is calculated only if more than a certain
percentage of the corresponding 30 minutes data is present. b) Relative difference in the number of entries of available data for the 180 minutes average compared to the
30 minutes average.
'''

PLOT_TYPE = 'nbr-of-entries'



for sampling_percentage in SAMPLING_PERCENTAGES :

    for min_nbr_yrs in MIN_NBR_YRS :


        # Step 1 : Obtain station numbers, ids and station filepaths

        station_names_file_pathname = SNOW_DILUCA_DIRECTORY + SAMPLING_PERCENTAGE_DIRECTORY + sampling_percentage + SLASH_BAR + MIN_NBR_YRS_DIRECTORY + min_nbr_yrs + SLASH_BAR + STATION_NAMES_FILENAME
        station_names_file          = open(station_names_file_pathname, READING_CHAR)

        station_nbrs_list         = []
        station_ids_list          = []
        dates_3_hr_filepaths_list = []

        for station_names_line in station_names_file :

            amf_filename        = os.path.basename(station_names_line)
            station_nbr         = amf_filename.split(STATION_NAMES_DELIMITER)[STATION_NBR_INDEX]
            station_id          = amf_filename.split(STATION_NAMES_DELIMITER)[STATION_ID_INDEX]
            dates_3_hr_filepath = station_names_line.replace(NEW_LINE_CHAR, NULL_CHAR).replace(SLASH_BAR+SLASH_BAR, SLASH_BAR).replace(DATA_ID, DATES_ID)

            station_nbrs_list.append(station_nbr)
            station_ids_list.append(station_id)
            dates_3_hr_filepaths_list.append(dates_3_hr_filepath)

        station_names_file.close()
        #pdb.set_trace()


        # Step 2 : Obtain number of entries for 0.5 and 3 hour averages 

        nbr_of_entries_0_5_hr_list = []
        nbr_of_entries_3_hr_list   = []

        for dates_3_hr_filepath, station_id in zip(dates_3_hr_filepaths_list, station_ids_list) :

            dates_3_hr          = np.load(dates_3_hr_filepath)
            nbr_of_entries_3_hr = dates_3_hr.shape[DATE_INDEX]

            dates_0_5_hr_filepath_pattern = SNOW_COMEAU_DIRECTORY + NUMPY_DIRECTORY + SLASH_BAR + STAR + DATES_ID + STAR + station_id + STAR
            dates_0_5_hr_filepath         = glob.glob(dates_0_5_hr_filepath_pattern)[FILEPATH_INDEX]
            dates_0_5_hr                  = np.load(dates_0_5_hr_filepath)
            nbr_of_entries_0_5_hr         = dates_0_5_hr.shape[DATE_INDEX]

            nbr_of_entries_3_hr_list.append(nbr_of_entries_3_hr)
            nbr_of_entries_0_5_hr_list.append(nbr_of_entries_0_5_hr)
            #pdb.set_trace()


        # Step 3 : Produce plot comparing number of entries
            
        min_nbr_data                = MIN_NBR_DATA[ SAMPLING_PERCENTAGES.index(sampling_percentage) ]
        nbr_of_entries_3_hr_label   = NBR_OF_ENTRIES_3_HR_LABEL_1 + min_nbr_yrs + NBR_OF_ENTRIES_3_HR_LABEL_2 + min_nbr_data + NBR_OF_ENTRIES_3_HR_LABEL_3
        station_numbers_array       = np.array(station_nbrs_list)
        station_names_array         = np.array(station_ids_list)
        nbr_of_entries_0_5_hr_array = np.array(nbr_of_entries_0_5_hr_list)
        nbr_of_entries_3_hr_array   = np.array(nbr_of_entries_3_hr_list)

        plot_filename = PLOT_TYPE + SAMPLING_PERCENTAGE_DIRECTORY.replace(SLASH_BAR, STATION_NAMES_DELIMITER) + sampling_percentage + MIN_NBR_YRS_DIRECTORY.replace(SLASH_BAR, STATION_NAMES_DELIMITER) + min_nbr_yrs + PNG_SUFFIX
        plot_pathname = SNOW_COMEAU_DIRECTORY + PNG_DIRECTORY + SLASH_BAR + plot_filename

        mcp.Make_comparison_plot(station_numbers_array, station_names_array, nbr_of_entries_0_5_hr_array, nbr_of_entries_3_hr_array, NBR_OF_ENTRIES_Y_AXIS_LABEL, NBR_OF_ENTRIES_0_5_HR_LABEL, nbr_of_entries_3_hr_label, plot_pathname)
        #pdb.set_trace()
