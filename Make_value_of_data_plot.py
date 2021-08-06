import os
import glob
import numpy as np
import Make_time_series_plot as mtsp
import sys
import pdb


"""

This script produces a time series plot showing the value of the energy balance variables for a given station according to the sampling percentage used to produce the 3 hour means from the 30 minute mean. 
The time series covers roughly the first three days of data. One plot per station per variable.


Author        : Élise Comeau

Created       : July 28th, 2021

Last modified : August 5th, 2021

"""

# Step 0 : Define constants

# Step 0.1 : Define directories

HALF_HR_DIRECTORY     = '/snow/comeau/FLUXNET_America/AMF_1990-2017/npy'
MIN_NBR_YRS_DIRECTORY = '/num-years1'
NUMPY_DIRECTORY       = '/npy'
PLOT_DIRECTORY        = '/snow/comeau/FLUXNET_America/AMF_1990-2017/png'
THREE_HR_DIRECTORY    = '/snow/diluca/FLUXNET_America/1990-2017/v3/TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE/sampling-percentage'


# Step 0.2 : Define filenames

STATION_NAMES_FILENAME = 'AMF_station-filelist_1990-2017_TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE.txt'


# Step 0.3 : Define prefixes and suffixes

AMF_PREFIX = 'AMF_'
PNG_SUFFIX = '.png'
TXT_SUFFIX = '.txt'


# Step 0.4 : Define delimiters

STATION_NAMES_DELIMITER = '_'
VAR_NAMES_DELIMITER     = '-'


# Step 0.5 : Define special characters

NULL_CHAR    = ''
READING_CHAR = 'r'
SLASH_BAR    = '/'
STAR         = '*'


# Step 0.6 : Define indexes

FILEPATH_INDEX    = 0
FIRST_ITEM_INDEX  = 0
STATION_ID_INDEX  = 3
STATION_NBR_INDEX = 2
VAR_NAMES_INDEX   = 3


# Step 0.7 : Define values

DATA_ID              = 'data'
DATES_ID             = 'dates'
SAMPLING_PERCENTAGES = ['10', '25', '50', '60', '75', '100']  # minimum sampling percentages
MIN_NBR_DATA         = ['1', '2', '3', '4', '5', '6']


# Step 0.8 : Define plot constants

HALF_HR_LEGEND_LABEL    = 'AMF -  30 mins'
THREE_HR_LEGEND_LABEL_1 = 'AMF - 180 mins ('
THREE_HR_LEGEND_LABEL_2 = '/6+ data)'
PLOT_TYPE               = 'var-values'



# Step 1 : Obtain variables of interest

var_names       = STATION_NAMES_FILENAME.split(STATION_NAMES_DELIMITER, VAR_NAMES_INDEX)[VAR_NAMES_INDEX].replace(TXT_SUFFIX, NULL_CHAR)
var_names_list  = var_names.split(VAR_NAMES_DELIMITER)



# Step 2 : Obtain station numbers and ids

station_names_file_pathname = THREE_HR_DIRECTORY + SAMPLING_PERCENTAGES[0] + MIN_NBR_YRS_DIRECTORY + SLASH_BAR + STATION_NAMES_FILENAME
station_names_file          = open(station_names_file_pathname, READING_CHAR)

station_nbrs_list         = []
station_ids_list          = []

for station_names_line in station_names_file :

    amf_filename        = os.path.basename(station_names_line)
    station_nbr         = amf_filename.split(STATION_NAMES_DELIMITER)[STATION_NBR_INDEX]
    station_id          = amf_filename.split(STATION_NAMES_DELIMITER)[STATION_ID_INDEX]

    station_ids_list.append(station_id)
    station_nbrs_list.append(station_nbr)

station_names_file.close()



# Step 3 : Obtain dates and data for plot

for station_id, station_nbr in zip(station_ids_list, station_nbrs_list) :

    station_dates_list = []
    station_data_list  = []
    labels_list        = []


    # Step 3.1 : Obtain dates and data for 0.5 hour average

    dates_0_5_hr_filepath_pattern = HALF_HR_DIRECTORY + SLASH_BAR + STAR + DATES_ID + STAR + station_id + STAR
    dates_0_5_hr_filepath         = glob.glob(dates_0_5_hr_filepath_pattern)[FILEPATH_INDEX]
    dates_0_5_hr                  = np.load(dates_0_5_hr_filepath)

    data_0_5_hr_filepath_pattern = dates_0_5_hr_filepath_pattern.replace(DATES_ID, DATA_ID)
    data_0_5_hr_filepath         = glob.glob(data_0_5_hr_filepath_pattern)[FILEPATH_INDEX]
    data_0_5_hr                  = np.load(data_0_5_hr_filepath)

    station_dates_list.append(dates_0_5_hr)
    station_data_list.append(data_0_5_hr)
    labels_list.append(HALF_HR_LEGEND_LABEL)


    # Step 3.2 : Obtain dates and data for 3 hour averages

    for sampling_percentage in SAMPLING_PERCENTAGES :

        dates_3_hr_filepath_pattern = THREE_HR_DIRECTORY + sampling_percentage + MIN_NBR_YRS_DIRECTORY + NUMPY_DIRECTORY + SLASH_BAR + AMF_PREFIX + DATES_ID + STAR + station_id + STAR

        dates_3_hr_files = glob.glob(dates_3_hr_filepath_pattern)

        if ( dates_3_hr_files ) :

            dates_3_hr_filepath = glob.glob(dates_3_hr_filepath_pattern)[FILEPATH_INDEX]
            dates_3_hr          = np.load(dates_3_hr_filepath)

            data_3_hr_filepath_pattern = dates_3_hr_filepath_pattern.replace(DATES_ID, DATA_ID)
            data_3_hr_filepath         = glob.glob(data_3_hr_filepath_pattern)[FILEPATH_INDEX]
            data_3_hr                  = np.load(data_3_hr_filepath)

            min_nbr_data      = MIN_NBR_DATA[SAMPLING_PERCENTAGES.index(sampling_percentage)]
            values_3_hr_label = THREE_HR_LEGEND_LABEL_1 + min_nbr_data + THREE_HR_LEGEND_LABEL_2

            station_dates_list.append(dates_3_hr)
            station_data_list.append(data_3_hr)
            labels_list.append(values_3_hr_label)


    # Step 4 : Create plots

    for var_name in var_names_list :

        var_index     = var_names_list.index(var_name)
        nbr_of_combos = len(station_data_list)          # combos refers to combinations of sampling percentages and minimum numbers of years of data

        station_data_ploting_list = []

        for combo_nbr in range(0, nbr_of_combos) :
            station_data_ploting_list.append(station_data_list[combo_nbr][:, var_index])

        plot_filename = PLOT_TYPE + STATION_NAMES_DELIMITER + station_nbr + STATION_NAMES_DELIMITER + station_id + STATION_NAMES_DELIMITER + var_name + STATION_NAMES_DELIMITER + MIN_NBR_YRS_DIRECTORY.replace(SLASH_BAR, NULL_CHAR) + PNG_SUFFIX
        plot_pathname = PLOT_DIRECTORY + SLASH_BAR + plot_filename

        mtsp.Make_time_series_plot(station_dates_list, station_data_ploting_list, labels_list, var_name, plot_pathname)
