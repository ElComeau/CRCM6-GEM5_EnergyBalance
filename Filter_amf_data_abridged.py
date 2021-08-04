import os
import glob
import fluxnet_classes as fc
import numpy as np
import datetime
import Make_comparison_plots_v4 as mcp
import pdb


'''
This scripts processes AmeriFlux (AMF) data at a 0.5 hour frequency. It removes unnecessary variables and data entries with missing values.
'''


# Step 0 : Define constants

# Step 0.1 : Define directories

DATA_VALIDATION_DIRECTORY     = '/home/data/Validation/AmeriFlux'
MIN_NBR_YRS_DIRECTORY         = '/num-years'
NUMPY_DIRECTORY               = '/npy'
SAMPLING_PERCENTAGE_DIRECTORY = '/sampling-percentage'
SNOW_COMEAU_DIRECTORY         = '/snow/comeau/FLUXNET_America/AMF_1990-2017'
SNOW_DILUCA_DIRECTORY         = '/snow/diluca/FLUXNET_America/1990-2017/v1/TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE'


# Step 0.2 : Define filenames

DATES_0_5_HR_FILENAME_1 = 'AMF_dates_'
DATES_0_5_HR_FILENAME_2 = '_1990-2017_'
DATES_0_5_HR_FILENAME_3 = '_0-5.npy'
STATION_NAMES_FILENAME  = 'AMF_station-filelist_1990-2017_TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE.txt'
SUMMARY_FILENAME        = 'AMF_summary_1990-2021_TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE.txt'


# Step 0.3 : Define delimiters

DATES_AND_DATA_0_5_HR_DELIMITER = ','
STATION_NAMES_DELIMITER         = '_'
VAR_NAMES_DELIMITER             = '-'


# Step 0.4 : Define prefixes and suffixes

AMF_PREFIX = 'AMF_'
CSV_SUFFIX = '.csv'
TXT_SUFFIX = '.txt'


# Step 0.5 : Define special characters

NEW_LINE_CHAR = '\n'
NULL_CHAR     = ''
READING_CHAR  = 'r'
SLASH_BAR     = '/'
STAR          = '*'


# Step 0.6 : Define indexes

DATES_0_5_HR_INDEX                   = 0
DATES_3_HR_INDEX                     = 0
DATES_AND_DATA_0_5_HR_PATHNAME_INDEX = 0
DATES_AND_DATA_3_HR_PATHNAME_INDEX   = 0
STATION_ID_INDEX                     = 3
STATION_NBR_INDEX                    = 2
VAR_NAMES_INDEX                      = 3


# Step 0.7 : Define values

DATA_ID                               = 'data'
DATES_0_5_HR_FORMAT                   = '%Y%m%d%H%M'
DATES_0_5_HR_HALF_TIME                = 15                  # half of half an hour is 15 minutes
DATES_AND_DATA_0_5_NBR_OF_HEADER_ROWS = 3
DATES_ID                              = 'dates'
MIN_NBR_YRS                           = ['1', '2', '5']     # minimum number of years of available data
MISSING_VALUE                         = '-9999'
SAMPLING_PERCENTAGES                  = ['25', '50', '75']  # minimum sampling percentages
T_FREQ                                = 0.5                 # in hours



# Step 1 : Obtain variables of interest

var_names      = STATION_NAMES_FILENAME.split(STATION_NAMES_DELIMITER, VAR_NAMES_INDEX)[VAR_NAMES_INDEX].replace(TXT_SUFFIX, NULL_CHAR)
var_names_list = var_names.split(VAR_NAMES_DELIMITER)
#pdb.set_trace()



# Step 2 : Obtain station numbers and ids

station_names_file_pathname = SNOW_COMEAU_DIRECTORY + SLASH_BAR + STATION_NAMES_FILENAME
station_names_file          = open(station_names_file_pathname, READING_CHAR)

station_nbrs_list = []
station_ids_list  = []

for station_names_line in station_names_file :

    amf_filename = os.path.basename(station_names_line)
    station_nbr  = amf_filename.split(STATION_NAMES_DELIMITER)[STATION_NBR_INDEX]
    station_id   = amf_filename.split(STATION_NAMES_DELIMITER)[STATION_ID_INDEX]

    station_nbrs_list.append(station_nbr)
    station_ids_list.append(station_id)

station_names_file.close()
#pdb.set_trace()



# Step 3 : Process dates and data for 0.5 hour averages

total_dates_0_5_hr_list    = []
nbr_of_entries_0_5_hr_list = []

for station_nbr, station_id in zip(station_nbrs_list, station_ids_list) :


    # Step 3.1 : Obtain file for the 0.5 hour average dates and data

    dates_and_data_0_5_hr_pathname_pattern = DATA_VALIDATION_DIRECTORY + SLASH_BAR + AMF_PREFIX + station_id + STAR + CSV_SUFFIX
    dates_and_data_0_5_hr_pathname         = glob.glob(dates_and_data_0_5_hr_pathname_pattern)[DATES_AND_DATA_0_5_HR_PATHNAME_INDEX]
    dates_and_data_0_5_hr_file             = open(dates_and_data_0_5_hr_pathname, READING_CHAR)
    #pdb.set_trace()


    # Step 3.2 : Obtain variables for 0.5 hour average dates and data files

    for line_nbr in range(0, DATES_AND_DATA_0_5_NBR_OF_HEADER_ROWS - 1) :
        dates_and_data_0_5_hr_file.readline()

    data_0_5_hr_var_names                                   = dates_and_data_0_5_hr_file.readline().split(DATES_AND_DATA_0_5_HR_DELIMITER)
    data_0_5_hr_var_names[ len(data_0_5_hr_var_names) - 1 ] = data_0_5_hr_var_names[ len(data_0_5_hr_var_names) - 1].replace(NEW_LINE_CHAR, NULL_CHAR)
    #pdb.set_trace()


    # Step 3.3 : Extract relevant dates and data for 0.5 hour averages

    data_0_5_hr_list  = []
    dates_0_5_hr_list = []

    for dates_and_data_0_5_hr_line in dates_and_data_0_5_hr_file :

        data_0_5_hr_line_list = []

        for var_name in var_names_list :

            var_index = data_0_5_hr_var_names.index(var_name)
            var_value = dates_and_data_0_5_hr_line.split(DATES_AND_DATA_0_5_HR_DELIMITER)[var_index].replace(NEW_LINE_CHAR, NULL_CHAR)

            if ( var_value == MISSING_VALUE ) :  # if at least one value is missing ...
                break                            # ... then the entire line is not worth keeping

            else :
                data_0_5_hr_line_list.append(float(var_value))

        if ( len(data_0_5_hr_line_list) == len(var_names_list) ) :  # so as to not append an incomplete list

            date_0_5_hr_string           = dates_and_data_0_5_hr_line.split(DATES_AND_DATA_0_5_HR_DELIMITER)[DATES_0_5_HR_INDEX]
            date_0_5_hr_datetime         = datetime.datetime.strptime(date_0_5_hr_string, DATES_0_5_HR_FORMAT)
            date_0_5_hr_central_datetime = date_0_5_hr_datetime + datetime.timedelta(minutes=DATES_0_5_HR_HALF_TIME)
            date_0_5_hr_elapsed_time     = (date_0_5_hr_central_datetime - fc.constants.reference_date).total_seconds()

            dates_0_5_hr_list.append(date_0_5_hr_elapsed_time)
            data_0_5_hr_list.append(data_0_5_hr_line_list)
            #pdb.set_trace()

    total_dates_0_5_hr_list.append(len(dates_0_5_hr_list))
    nbr_of_entries_0_5_hr_list.append(len(dates_0_5_hr_list))
    #pdb.set_trace()


    # Step 3.4 : Save relevant dates and data for 0.5 hour average

    dates_0_5_hr_array    = np.asarray(dates_0_5_hr_list)
    dates_0_5_hr_filename = DATES_0_5_HR_FILENAME_1 + station_nbr + STATION_NAMES_DELIMITER + station_id + DATES_0_5_HR_FILENAME_2 + var_names + DATES_0_5_HR_FILENAME_3
    dates_0_5_hr_pathname = SNOW_COMEAU_DIRECTORY + NUMPY_DIRECTORY + SLASH_BAR + dates_0_5_hr_filename

    np.save(dates_0_5_hr_pathname, dates_0_5_hr_array)

    data_0_5_hr_array    = np.asarray(data_0_5_hr_list)
    data_0_5_hr_pathname = dates_0_5_hr_pathname.replace(DATES_ID, DATA_ID)

    np.save(data_0_5_hr_pathname, data_0_5_hr_array)
    #pdb.set_trace()


# Step 3.5 : Save number of years of data for 0.5 hour average

dates_0_5_hr_t_freq = [ T_FREQ ] * len(total_dates_0_5_hr_list)

total_dates_filename = SUMMARY_FILENAME
total_dates_filepath = SNOW_COMEAU_DIRECTORY + SLASH_BAR + SUMMARY_FILENAME

fc.print_summary(total_dates_0_5_hr_list, total_dates_filepath, dates_0_5_hr_t_freq, var_names)
