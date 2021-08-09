import os
import glob
import numpy as np
import sys
import Make_comparative_bar_plot as mcbp
import pdb

"""

This script produces a plot showing the amount of data present at each AmeriFlux (AMF) station according to the minimum sampling percentage used to produce the 3 hour means from the 30 minute means.
The plot contains two subplots, both of which are comparative barplots. The first barplot shows the ratio between the amount of 30 mins means over the amount of 3 hour means per station and per minimum sampling percentage.
The second subplot shows the amount of years of 3 hour data available per station and per minimum sampling percentages.
The plot is saved to a file.


Author        : Élise Comeau

Created       : July 27th, 2021

Last modified : August 9th, 2021

"""


# Step 0 : Define constants

# Step 0.1 : Define directories

INPUT_DIRECTORY_1 = '/snow/diluca/FLUXNET_America/1990-2017/v3/TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE/sampling-percentage'
INPUT_DIRECTORY_2 = '/num-years1'
INPUT_DIRECTORY_3 = '/npy'
OUTPUT_DIRECTORY  = '/snow/comeau/FLUXNET_America/AMF_1990-2017/png'


# Step 0.2 : Define filenames

STATION_NAMES_FILENAME = 'AMF_station-filelist_1990-2017_TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE.txt'
SUMMARY_FILENAME       = 'AMF_summary_1990-2017_TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE.txt'


# Step 0.3 : Define prefixes and suffixes

HALF_HR_SUFFIX  = '_30.npy'
THREE_HR_SUFFIX = '_3.npy'
PNG_SUFFIX      = '.png'


# Step 0.4 : Define delimiters

STATION_NAMES_DELIMITER        = '_'
STATION_NBRS_AND_IDS_DELIMITER = ' '
YRS_OF_DATA_DELIMITER          = ' '


# Step 0.5 : Define special characters

COLON_CHAR    = ':'
NEW_LINE_CHAR = '\n'
NULL_CHAR     = ''
READING_CHAR  = 'r'
SLASH_BAR     = '/'
STAR          = '*'


# Step 0.6 : Define indexes

DATE_INDEX          = 0
FILEPATH_INDEX      = 0
FIRST_ITEM_INDEX    = 0
STATION_ID_INDEX    = 3
STATION_NBR_INDEX_1 = 2
STATION_NBR_INDEX_2 = 2
YRS_OF_DATA_INDEX   = 4


# Step 0.7 : Define values

DATA_ID              = 'data'
DATES_ID             = 'dates'
MIN_NBR_DATA         = ['1', '2', '3', '4', '5', '6']
NBR_OF_HEADER_ROWS   = 3
ROUNDING_POSITION    = 3
SAMPLING_PERCENTAGES = ['10', '25', '50', '60', '75', '100']  # minimum sampling percentages
STATION_STR_1        = 'Station '
STATION_STR_2        = ':'


# Step 0.7 : Define plot constants

ENTRY_RATIOS_Y_AXIS_LABEL                   = 'amount of entries ratio (30 mins / 180 mins)'
YRS_OF_DATA_Y_AXIS_LABEL                    = 'amount of years of data (180 mins avg)'
ENTRY_RATIOS_AND_YRS_OF_DATA_LEGEND_LABEL_1 = 'AMF - ('
ENTRY_RATIOS_AND_YRS_OF_DATA_LEGEND_LABEL_2 = '/6+ data)'
PLOT_TYPE                                   = 'amount-of-entries-ratio-and-yrs'
X_AXIS_LABEL                                = 'site of measurement'


# Step 1 : Obtain station ids and numbers

station_ids_file_pathname = INPUT_DIRECTORY_1 + SAMPLING_PERCENTAGES[0] + INPUT_DIRECTORY_2 + SLASH_BAR + STATION_NAMES_FILENAME
station_ids_file          = open(station_ids_file_pathname, READING_CHAR)

station_ids_list  = []
station_nbrs_list = []

for station_ids_line in station_ids_file :

    station_filename = os.path.basename(station_ids_line)
    station_id       = station_filename.split(STATION_NAMES_DELIMITER)[STATION_ID_INDEX]
    station_nbr      = station_filename.split(STATION_NAMES_DELIMITER)[STATION_NBR_INDEX_1]

    station_ids_list.append(station_id)
    station_nbrs_list.append(station_nbr)

station_ids_file.close()


# Step 2 : Obtain station filenames

entry_ratios_all_stations = []
yrs_of_data_all_stations  = []

entry_ratios_and_yrs_of_data_legend_labels = []

for sampling_percentage in SAMPLING_PERCENTAGES :

    station_pathnames_file_pathname = INPUT_DIRECTORY_1 + sampling_percentage + INPUT_DIRECTORY_2 + SLASH_BAR + STATION_NAMES_FILENAME
    station_pathnames_file          = open(station_pathnames_file_pathname)
    station_pathnames               = station_pathnames_file.readlines()

    yrs_of_data_pathname = INPUT_DIRECTORY_1 + sampling_percentage + INPUT_DIRECTORY_2 + SLASH_BAR + SUMMARY_FILENAME
    yrs_of_data_file     = open(yrs_of_data_pathname)
    yrs_of_data_content  = yrs_of_data_file.readlines()

    entry_ratios_per_station = []
    yrs_of_data_per_station  = []

    for station_id in station_ids_list :

        station_filepath = [ station_pathname for station_pathname in station_pathnames if station_id in station_pathname ] 

        if ( station_filepath ) :


            # Step 3 : Obtain ratios of amount of entries (half hour over 3 hour averages)

            three_hr_dates_filepath = station_filepath[FIRST_ITEM_INDEX].replace(NEW_LINE_CHAR, NULL_CHAR).replace(SLASH_BAR+SLASH_BAR, SLASH_BAR).replace(DATA_ID, DATES_ID)                        

            three_hr_dates             = np.load(three_hr_dates_filepath)
            three_hr_amount_of_entries = three_hr_dates.shape[DATE_INDEX]

            half_hr_dates_filepath    = three_hr_dates_filepath.replace(THREE_HR_SUFFIX, HALF_HR_SUFFIX)
            half_hr_dates             = np.load(half_hr_dates_filepath)
            half_hr_amount_of_entries = half_hr_dates.shape[DATE_INDEX]

            entry_ratio = round( (half_hr_amount_of_entries / three_hr_amount_of_entries), ROUNDING_POSITION)



            # Step 4 : Obtain number of years of data for 3 hour averages

            station_nbr             = int( os.path.basename(three_hr_dates_filepath).split(STATION_NAMES_DELIMITER)[STATION_NBR_INDEX_2] )
            station_str             = STATION_STR_1 + str(station_nbr) + STATION_STR_2   
            station_yrs_of_data_str = [ yrs_of_data_item for yrs_of_data_item in yrs_of_data_content if station_str in yrs_of_data_item ]

            yrs_of_data = float( station_yrs_of_data_str[FIRST_ITEM_INDEX].split(YRS_OF_DATA_DELIMITER)[YRS_OF_DATA_INDEX].replace(NEW_LINE_CHAR, NULL_CHAR) )

        else :

            entry_ratio = 0
            yrs_of_data = 0

        entry_ratios_per_station.append(entry_ratio)
        yrs_of_data_per_station.append(yrs_of_data)

    station_pathnames_file.close()
    yrs_of_data_file.close()

    entry_ratios_all_stations.append(entry_ratios_per_station)
    yrs_of_data_all_stations.append(yrs_of_data_per_station)

    min_nbr_of_data                           = MIN_NBR_DATA[ SAMPLING_PERCENTAGES.index(sampling_percentage) ]
    entry_ratios_and_yrs_of_data_legend_label = ENTRY_RATIOS_AND_YRS_OF_DATA_LEGEND_LABEL_1 + min_nbr_of_data + ENTRY_RATIOS_AND_YRS_OF_DATA_LEGEND_LABEL_2 

    entry_ratios_and_yrs_of_data_legend_labels.append(entry_ratios_and_yrs_of_data_legend_label)


# Step 4 : Produce plot of ratios and number of years of data
     
station_nbrs_and_ids = []

for station_nbr, station_id in zip( station_nbrs_list, station_ids_list ) :

    station_nbr_and_id = station_nbr + STATION_NBRS_AND_IDS_DELIMITER + station_id

    station_nbrs_and_ids.append(station_nbr_and_id)

plot_filename = PLOT_TYPE + INPUT_DIRECTORY_2.replace(SLASH_BAR, STATION_NAMES_DELIMITER) + PNG_SUFFIX
plot_pathname = OUTPUT_DIRECTORY + SLASH_BAR + plot_filename

mcbp.Make_comparative_bar_plot(station_nbrs_and_ids, entry_ratios_all_stations, yrs_of_data_all_stations, X_AXIS_LABEL, ENTRY_RATIOS_Y_AXIS_LABEL, YRS_OF_DATA_Y_AXIS_LABEL, entry_ratios_and_yrs_of_data_legend_labels, entry_ratios_and_yrs_of_data_legend_labels, plot_pathname)
