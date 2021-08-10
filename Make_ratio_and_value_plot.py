import os
import glob
import numpy as np
import sys
import Calculate_stats as cs
import Make_comparative_bar_plot as mcbp
import fluxnet_classes as fc
import pdb

"""

This script produces a plot showing the amount of data present and its value at each AmeriFlux (AMF) station according to the minimum sampling percentage used to produce the 3 hour means from the 30 
minute means. The plot contains two subplots, both of which are comparative barplots. The first barplot shows the ratio between the amount of 30 mins means over the amount of 3 hour means per station
and per minimum sampling percentage. The second subplot shows the value of a variable per station and per minimum sampling percentages.
The plot is saved to a file.


Author        : Élise Comeau

Created       : August 10th, 2021

Last modified : August 10th, 2021

"""


# Step 0 : Define constants

# Step 0.1 : Define directories

INPUT_DIRECTORY_1 = '/snow/diluca/FLUXNET_America/1990-2017/v3/TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE/sampling-percentage'
INPUT_DIRECTORY_2 = '/num-years1'
OUTPUT_DIRECTORY  = '/snow/comeau/FLUXNET_America/AMF_1990-2017/png'


# Step 0.2 : Define filenames

STATION_NAMES_FILENAME = 'AMF_station-filelist_1990-2017_TA-SW_IN-SW_OUT-LW_IN-LW_OUT-H-LE.txt'


# Step 0.3 : Define prefixes and suffixes

HALF_HR_SUFFIX  = '_30.npy'
THREE_HR_SUFFIX = '_3.npy'
TXT_SUFFIX      = '.txt'
PNG_SUFFIX      = '.png'


# Step 0.4 : Define delimiters

STATION_NAMES_DELIMITER        = '_'
STATION_NBRS_AND_IDS_DELIMITER = ' '
VAR_NAMES_DELIMITER            = '-'


# Step 0.5 : Define special characters

NEW_LINE_CHAR = '\n'
NULL_CHAR     = ''
READING_CHAR  = 'r'
SLASH_BAR     = '/'
#STAR          = '*'


# Step 0.6 : Define indexes

DATA_INDEX        = 0
FIRST_ITEM_INDEX  = 0
STATION_ID_INDEX  = 3
STATION_NBR_INDEX = 2
VAR_NAMES_INDEX   = 3


# Step 0.7 : Define values

MIN_NBR_DATA         = ['1', '2', '3', '4', '5', '6']
TYPE_OF_STAT         = ['MEAN']
ROUNDING_POSITION    = 3
SAMPLING_PERCENTAGES = ['10', '25', '50', '60', '75', '100']  # minimum sampling percentages


# Step 0.7 : Define plot constants

ENTRY_RATIOS_Y_AXIS_LABEL                   = 'amount of entries ratio (30 mins / 180 mins)'
MEAN_VALUE_Y_AXIS_LABEL                     = 'mean value of '
ENTRY_RATIOS_AND_YRS_OF_DATA_LEGEND_LABEL_1 = 'AMF - ('
ENTRY_RATIOS_AND_YRS_OF_DATA_LEGEND_LABEL_2 = '/6+ data)'
PLOT_TYPE                                   = 'amount-of-entries-ratio-and-mean-values'
X_AXIS_LABEL                                = 'site of measurement'



# Step 1 : Obtain variables of interest

var_names	= STATION_NAMES_FILENAME.split(STATION_NAMES_DELIMITER, VAR_NAMES_INDEX)[VAR_NAMES_INDEX].replace(TXT_SUFFIX, NULL_CHAR)
var_names_list  = var_names.split(VAR_NAMES_DELIMITER)
nbr_of_vars     = len(var_names_list)



# Step 2 : Obtain station ids and numbers

station_ids_file_pathname = INPUT_DIRECTORY_1 + SAMPLING_PERCENTAGES[0] + INPUT_DIRECTORY_2 + SLASH_BAR + STATION_NAMES_FILENAME
station_ids_file          = open(station_ids_file_pathname, READING_CHAR)

station_ids_list  = []
station_nbrs_list = []

for station_ids_line in station_ids_file :

    station_filename = os.path.basename(station_ids_line)
    station_id       = station_filename.split(STATION_NAMES_DELIMITER)[STATION_ID_INDEX]
    station_nbr      = station_filename.split(STATION_NAMES_DELIMITER)[STATION_NBR_INDEX]

    station_ids_list.append(station_id)
    station_nbrs_list.append(station_nbr)

station_ids_file.close()



# Step 3 : Obtain station filenames

entry_ratios_all_stations       = []
mean_value_of_data_all_stations = []

entry_ratios_and_yrs_of_data_legend_labels = []

for sampling_percentage in SAMPLING_PERCENTAGES :

    station_pathnames_file_pathname = INPUT_DIRECTORY_1 + sampling_percentage + INPUT_DIRECTORY_2 + SLASH_BAR + STATION_NAMES_FILENAME
    station_pathnames_file          = open(station_pathnames_file_pathname)
    station_pathnames               = station_pathnames_file.readlines()

    entry_ratios_per_station       = []
    mean_value_of_data_per_station = []

    for station_id in station_ids_list :

        station_filepath = [ station_pathname for station_pathname in station_pathnames if station_id in station_pathname ] 

        if ( station_filepath ) :


            # Step 4 : Obtain ratios of amount of entries (half hour over 3 hour averages)

            three_hr_data_filepath = station_filepath[FIRST_ITEM_INDEX].replace(NEW_LINE_CHAR, NULL_CHAR).replace(SLASH_BAR+SLASH_BAR, SLASH_BAR)

            three_hr_data              = np.load(three_hr_data_filepath)
            three_hr_amount_of_entries = three_hr_data.shape[DATA_INDEX]

            half_hr_data_filepath     = three_hr_data_filepath.replace(THREE_HR_SUFFIX, HALF_HR_SUFFIX)
            half_hr_data              = np.load(half_hr_data_filepath)
            half_hr_amount_of_entries = half_hr_data.shape[DATA_INDEX]

            entry_ratio = round( (half_hr_amount_of_entries / three_hr_amount_of_entries), ROUNDING_POSITION)



            # Step 5 : Calculate the mean value for each variable of interest

            mean_values_of_data = []

            for variable_index in range(nbr_of_vars) :

                data_values        = np.asarray( three_hr_data[:, variable_index] )
                mean_value_of_data = cs.Calculate_stats(TYPE_OF_STAT, data_values)

                mean_values_of_data.append( round(mean_value_of_data[0], ROUNDING_POSITION) )

        else :

            entry_ratio         = 0
            mean_values_of_data = nbr_of_vars * [0]            

        entry_ratios_per_station.append(entry_ratio)
        mean_value_of_data_per_station.append(mean_values_of_data)

    station_pathnames_file.close()

    entry_ratios_all_stations.append(entry_ratios_per_station)
    mean_value_of_data_all_stations.append(mean_value_of_data_per_station)

    min_nbr_of_data                           = MIN_NBR_DATA[ SAMPLING_PERCENTAGES.index(sampling_percentage) ]
    entry_ratios_and_yrs_of_data_legend_label = ENTRY_RATIOS_AND_YRS_OF_DATA_LEGEND_LABEL_1 + min_nbr_of_data + ENTRY_RATIOS_AND_YRS_OF_DATA_LEGEND_LABEL_2 

    entry_ratios_and_yrs_of_data_legend_labels.append(entry_ratios_and_yrs_of_data_legend_label)


# Step 6 : Produce plot of ratios and means of data
     
mean_value_of_data_all_stations_array = np.asarray(mean_value_of_data_all_stations)

station_nbrs_and_ids = []

for station_nbr, station_id in zip( station_nbrs_list, station_ids_list ) :

    station_nbr_and_id = station_nbr + STATION_NBRS_AND_IDS_DELIMITER + station_id

    station_nbrs_and_ids.append(station_nbr_and_id)

for var_index in range(nbr_of_vars) :

    var_name = var_names_list[var_index]

    mean_value_of_var_all_stations = mean_value_of_data_all_stations_array[:, :, var_index]

    mean_value_y_axis_label = MEAN_VALUE_Y_AXIS_LABEL + var_name + ' [' + fc.variables.units[var_name] + ']'

    plot_filename = PLOT_TYPE + INPUT_DIRECTORY_2.replace(SLASH_BAR, STATION_NAMES_DELIMITER) + STATION_NAMES_DELIMITER + var_name + PNG_SUFFIX
    plot_pathname = OUTPUT_DIRECTORY + SLASH_BAR + plot_filename

    mcbp.Make_comparative_bar_plot(station_nbrs_and_ids, entry_ratios_all_stations, mean_value_of_var_all_stations, X_AXIS_LABEL, ENTRY_RATIOS_Y_AXIS_LABEL, mean_value_y_axis_label, entry_ratios_and_yrs_of_data_legend_labels, entry_ratios_and_yrs_of_data_legend_labels, plot_pathname)
