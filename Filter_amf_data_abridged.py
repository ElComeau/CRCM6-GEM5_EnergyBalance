import os
import glob
import fluxnet_classes as fc
import numpy as np
import datetime
import pdb


"""

This scripts processes AmeriFlux (AMF) data at a 0.5 hour frequency in order to prepare it for use in different plotting scripts, namely Make_amount_of_data_plot.py and Make_value_of_data_plot.py.
It removes unnecessary variables (those not part of the energy balance) and data entries with at least one missing value. The processed data is saved to a .npy file.


Author        : Élise Comeau

Created       : July 28th, 2021

Last modified : August 5th, 2021

"""


# Step 0 : Define constants

# Step 0.1 : Define directories

DATES_AND_DATA_R_DIRECTORY = '/home/data/Validation/AmeriFlux'                 # 'R' for reading
DATES_AND_DATA_W_DIRECTORY = '/snow/comeau/FLUXNET_America/AMF_1990-2017/npy'  # 'W' for writing
MIN_NBR_YRS_DIRECTORY      = '/num-years1'
STATION_IDS_DIRECTORY      = '/snow/diluca/FLUXNET_America/1990-2017/v3/TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE/sampling-percentage'


# Step 0.2 : Define filenames

DATES_FILENAME_1       = 'AMF_dates_'
DATES_FILENAME_2       = '_1990-2017_'
DATES_FILENAME_3       = '_0-5.npy'
STATION_NAMES_FILENAME = 'AMF_station-filelist_1990-2017_TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE.txt'
SUMMARY_FILENAME       = 'AMF_summary_1990-2021_TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE.txt'


# Step 0.3 : Define delimiters

DATES_AND_DATA_DELIMITER = ','
STATION_IDS_DELIMITER    = '_'
VAR_NAMES_DELIMITER      = '-'


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

DATES_INDEX      = 0
PATHNAME_INDEX   = 0
STATION_ID_INDEX = 3
VAR_NAMES_INDEX  = 3


# Step 0.7 : Define values

DATA_ID              = 'data'
DATES_FORMAT         = '%Y%m%d%H%M'
DATES_ID             = 'dates'
HALF_HOURLY          = 'HH'
HALF_TIME            = 15                                     # half of 30 minutes os 15 minutes
MISSING_VALUE        = '-9999'                                # convention used in the AMF files
NBR_OF_HEADER_ROWS   = 3
SAMPLING_PERCENTAGES = ['10', '25', '50', '60', '75', '100']  # minimum sampling percentages
STATION_NBR_STR_LEN  = 3
T_FREQ               = 0.5                                    # in hours



# Step 1 : Obtain variables of interest

var_names_string = STATION_NAMES_FILENAME.split(STATION_IDS_DELIMITER, VAR_NAMES_INDEX)[VAR_NAMES_INDEX].replace(TXT_SUFFIX, NULL_CHAR)
var_names_list   = var_names_string.split(VAR_NAMES_DELIMITER)
#pdb.set_trace()



# Step 2 : Obtain station numbers and ids

station_ids_set = set()

for sampling_percentage in SAMPLING_PERCENTAGES :

    station_ids_file_pathname = STATION_IDS_DIRECTORY + sampling_percentage + MIN_NBR_YRS_DIRECTORY + SLASH_BAR + STATION_NAMES_FILENAME
    station_ids_file          = open(station_ids_file_pathname, READING_CHAR)

    for station_ids_file_line in station_ids_file :

        station_id = os.path.basename(station_ids_file_line).split(STATION_IDS_DELIMITER)[STATION_ID_INDEX]
        station_ids_set.add(station_id)
        #pdb.set_trace()

    station_ids_file.close()
    #pdb.set_trace()

station_ids_list = sorted(list(station_ids_set))
#pdb.set_trace()

station_nbrs_list = []

for station_nbr in np.arange(1, (len(station_ids_list) + 1)) :

    station_nbr_formatted = str(station_nbr).zfill(STATION_NBR_STR_LEN)
    station_nbrs_list.append(station_nbr_formatted)
    #pdb.set_trace()
#pdb.set_trace() 



# Step 3 : Process dates and data

total_dates_list = []

for station_nbr, station_id in zip(station_nbrs_list, station_ids_list) :


    # Step 3.1 : Obtain file for the dates and data

    dates_and_data_pathname_pattern = DATES_AND_DATA_R_DIRECTORY + SLASH_BAR + AMF_PREFIX + station_id + STAR + HALF_HOURLY + STAR + CSV_SUFFIX
    dates_and_data_pathname         = glob.glob(dates_and_data_pathname_pattern)[PATHNAME_INDEX]
    dates_and_data_file             = open(dates_and_data_pathname, READING_CHAR)
    #pdb.set_trace()


    # Step 3.2 : Obtain variables for the dates and data files

    for line_nbr in range(0, NBR_OF_HEADER_ROWS - 1) :
        dates_and_data_file.readline()

    var_names_in_file     = dates_and_data_file.readline().split(DATES_AND_DATA_DELIMITER)
    var_names_in_file_len = len(var_names_in_file)

    var_names_in_file[ var_names_in_file_len - 1 ] = var_names_in_file[ var_names_in_file_len - 1 ].replace(NEW_LINE_CHAR, NULL_CHAR)
    #pdb.set_trace()


    # Step 3.3 : Extract relevant dates and data

    data_list  = []
    dates_list = []

    for dates_and_data_line in dates_and_data_file :

        data_line_list = []

        for var_name in var_names_list :

            var_index = var_names_in_file.index(var_name)
            var_value = dates_and_data_line.split(DATES_AND_DATA_DELIMITER)[var_index].replace(NEW_LINE_CHAR, NULL_CHAR)

            if ( var_value == MISSING_VALUE ) :  # if at least one value is missing ...
                break                            # ... then the entire line is not worth keeping

            else :
                data_line_list.append( float(var_value) )

        if ( len(data_line_list) == len(var_names_list) ) :  # so as to not append an incomplete list

            date_string           = dates_and_data_line.split(DATES_AND_DATA_DELIMITER)[DATES_INDEX]
            date_datetime         = datetime.datetime.strptime(date_string, DATES_FORMAT)
            date_central_datetime = date_datetime + datetime.timedelta(minutes=HALF_TIME)
            date_elapsed_time     = (date_central_datetime - fc.constants.reference_date).total_seconds()

            dates_list.append(date_elapsed_time)
            data_list.append(data_line_list)
            #pdb.set_trace()

    total_dates_list.append(len(dates_list))
    #pdb.set_trace()


    # Step 3.4 : Save relevant dates and data

    dates_array    = np.array(dates_list)
    dates_filename = DATES_FILENAME_1 + station_nbr + STATION_IDS_DELIMITER + station_id + DATES_FILENAME_2 + var_names_string + DATES_FILENAME_3
    dates_pathname = DATES_AND_DATA_W_DIRECTORY + SLASH_BAR + dates_filename

    np.save(dates_pathname, dates_array)

    data_array    = np.array(data_list)
    data_pathname = dates_pathname.replace(DATES_ID, DATA_ID)

    np.save(data_pathname, data_array)
    #pdb.set_trace()


# Step 3.5 : Save number of years of data

t_freq_list = [ T_FREQ ] * len(total_dates_list)

total_dates_filename = SUMMARY_FILENAME
total_dates_filepath = DATES_AND_DATA_W_DIRECTORY + SLASH_BAR + SUMMARY_FILENAME

fc.print_summary(total_dates_list, total_dates_filepath, t_freq_list, var_names_string)
