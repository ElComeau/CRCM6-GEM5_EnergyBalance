import numpy as np
import sys
import glob
import re
import os
import matplotlib.pyplot as plt


# CONSTANTS

FILE_DIRECTORY        = '/snow/comeau/FLUXNET_America/1990-2019/npy/' # directory from which the input file is read and to which the output file(s) is/are written
DATA_FILENAME_PREFIX  = 'AMF_data_'                                   # prefix of the data file names to be read
DATES_FILENAME_PREFIX = 'AMF_dates_'                                  # prefix of the dates file names to be read

TEMPORAL_MEAN_PERIOD = 3 * 60 * 60                                    # period over which the temporal mean is done; in this case : 3 hours * 60 mins/h * 60 s/min = 10800 s
TEMPORAL_FREQUENCIES = np.array([1800, 3600])                         # accepted temporal frequencies for the input data, in seconds



def Temporal_mean(min_data_percentage, with_stats) :

    """

    Calculates the average over a given period of time from the average over a shorter period of time for a variety of atmospheric variables.    
    Calculates the mean and standard deviation for one or more variables in a data set before and after the temporal averaging, if requested.
    Saves the data and dates of the average over a given period in a file.
    Saves the mean and standard deviations in a file if their calculation was requested.
    Creates and saves a barplot of the means and standard deviations for each variable if these statistics were calculated. 
    

    Parameters :

        min_data_percentage (float) : Minimum amount of data required within a period for the mean to be calculated. Expressed as a percentage from 0 to 100.

        with_stats (boolean)        : Option to include the statistics. If 'True', the statistics will be calculated.


    Author        : Élise Comeau

    Created       : June 3rd, 2021

    Last modified : June 8th, 2021


    """


    # Step 1 : Validate the parameters

    with_stats = with_stats.capitalize()

    if ( (min_data_percentage <= 0) or (min_data_percentage > 100) ) :

        sys.exit('Minimum data percentage is invalid. Temporal mean will not be calculated.')

    elif ( (with_stats != 'True') and (with_stats != 'False') ) :

        sys.exit('Unable to determine if statistics must be calculated or not. Temporal mean will not be calculated.')

    else :


        # Step 2 : Obtain the list of files to read

        if ( with_stats == 'True' ) : # all the variables necessary for building the bar plot

            station_id_list  = []   # includes station number, country and station name
            mean_before_list = []
            mean_after_list  = []
            std_before_list  = []
            std_after_list   = []

        data_filenames_pattern  = FILE_DIRECTORY + DATA_FILENAME_PREFIX + '*'
        dates_filenames_pattern = FILE_DIRECTORY + DATES_FILENAME_PREFIX + '*'

        data_filenames  = glob.glob(data_filenames_pattern)
        dates_filenames = glob.glob(dates_filenames_pattern)

        nbr_of_stations = len(data_filenames)


        # Step 3 : Read the data and dates from the file

        for station in range(nbr_of_stations) :

            data_before  = np.load(data_filenames[station])
            dates_before = np.load(dates_filenames[station])


            # Step 4 : Extract and validate metadata

            filename        = os.path.splitext(os.path.basename(data_filenames[station]))[0]    # produces the filename without the directory path or the file extension
            t_freq          = int(filename.split('_')[ len(filename.split('_')) - 1 ])          # the time frequency corresponds to the last substring of the filename

            if ( station == 0 ) :

                filename_suffix = filename.split('_', 5)[5].split('-')                              # substring of the filename containing the variable names and t_freq
                var_names       = filename_suffix[0:(len(filename_suffix)-1)]                       # list of the variable names      

            if ( t_freq not in TEMPORAL_FREQUENCIES ) :

                print('Temporal frequency is not valid. Temporal mean will not be calculated for this dataset.\n')
                continue

            elif ( data_before.shape[0] != dates_before.shape[0] ) :

                print('The number of data and date entries do not match. Temporal mean will not be calculated.\n')
                continue

            else :


                # Step 5 : Calculate the statistics (mean and standard deviation) of the variable(s) before temporal averaging

                print('Data, dates and temporal frequency are in order. Temporal mean will be calculated.\n')

                if ( with_stats == 'True' ) :

                    split_filename = filename.split('_', 4)
                    station_id = split_filename[2] + '_' + split_filename[3]
                    station_id_list.append(station_id)

                    mean_before = np.array(np.mean(data_before, axis=0))
                    std_before  = np.array(np.std(data_before, axis=0))

                    mean_before_list.append(mean_before)
                    std_before_list.append(std_before)


                # Step 6 : Calculate averages for (nearly) contiguous entries

                contiguous_data  = []
                contiguous_dates = []
                total_rows       = data_before.shape[0]
                initial_time     = dates_before[0]                # time at which the period begins; we begin counting at the first row
                initial_row      = 0                              # row at which period begins        
                data_per_period  = TEMPORAL_MEAN_PERIOD / t_freq  # quantity of data per period, provided all the data is present
                offset           = 0                              # necessary to include the correct amount of rows in the mean calculation 

                for row in range(total_rows) :

                    time_difference = dates_before[row] - initial_time

                    if ( (time_difference >= TEMPORAL_MEAN_PERIOD) or (row == total_rows - 1) ) :

                        if ( row == (total_rows - 1) ) :
                            offset = 1

                        data_percentage = (row - initial_row + offset) / data_per_period * 100     # calculate the percentage of data that is present within the current period

                        if ( data_percentage >= min_data_percentage ) :

                            contiguous_data.append(np.mean(data_before[initial_row:row+offset,:], axis=0))  # data corresponds to the average of each variable (ie, column) for each entry per period
                            contiguous_dates.append(initial_time + TEMPORAL_MEAN_PERIOD / 2)                # dates correspond to the middle of the period

                        initial_time += TEMPORAL_MEAN_PERIOD
                        initial_row   = row

                data_after  = np.array(contiguous_data)
                dates_after = np.array(contiguous_dates)


                # Step 7 : Calculate the statistics (mean and standard deviation) of the variable(s) after temporal averaging

                if ( with_stats == 'True' ) :

                    mean_after = np.array(np.mean(data_after, axis=0))
                    std_after  = np.array(np.std(data_after, axis=0))

                    mean_after_list.append(mean_after)
                    std_after_list.append(std_after)


                # Step 8 : Write the results of the temporal averaging and the statistics (if applicable) to respective files

                data_filename  = filename.split('_', 1)[0] + '_temporal-avg_' + filename.split('_', 1)[1] + '.npy'
                dates_filename = data_filename.replace('data', 'dates')

                data_path  = os.path.join(FILE_DIRECTORY, data_filename)
                dates_path = os.path.join(FILE_DIRECTORY, dates_filename)

                np.save(data_path, data_after)
                np.save(dates_path, dates_after)

                if ( with_stats == 'True' ) :

                    mean_before_after = np.array([mean_before, mean_after])
                    std_before_after  = np.array([std_before, std_after])

                    mean_filename = data_filenames[station].replace('data', 'mean')
                    std_filename  = data_filenames[station].replace('data', 'std')

                    np.save(mean_filename, mean_before_after)
                    np.save(std_filename, std_before_after)



        # Step 9 : Create and save barplots for statistics

        if ( with_stats == 'True' ) :

            mean_before_array = np.array(mean_before_list)
            mean_after_array  = np.array(mean_after_list)
            std_before_array  = np.array(std_before_list)
            std_after_array   = np.array(std_after_list)

            nbr_of_vars = len(var_names)
            x_position  = np.arange(len(station_id_list))
            width       = 0.35                               # width of the bars

            for var in range(nbr_of_vars) :

                # barplot for mean

                mean_before = mean_before_array[:,var]
                mean_after  = mean_after_array[:,var] 

                fig, ax = plt.subplots(figsize=(10,4))

                bar_mean_before = ax.bar(x_position - width/2, mean_before, width, label='before temporal avg')
                bar_mean_after  = ax.bar(x_position + width/2, mean_after, width, label='after temporal avg')

                title = 'Mean of ' + var_names[var] + ' before and after averaging over a three hour period'
                ax.set_title(title)
                ax.set_xlabel('Station id')
                ax.set_ylabel('Mean')
                ax.set_xticks(x_position)
                ax.set_xticklabels(station_id_list, fontsize=9)
                plt.minorticks_on()
                ax.tick_params(axis='x', which='minor', bottom=False)
                plt.xticks(rotation=90)
                plt.grid(axis = 'y')
                ax.set_axisbelow(True)
                ax.legend()

                fig.tight_layout()

                filename      = 'AMF_temporal-avg_mean_1990-2019_' + var_names[var] + '.png'
                filedirectory = FILE_DIRECTORY.replace('npy', 'png') 
                filepath      = os.path.join(filedirectory, filename)  
                plt.savefig(filepath)


                # barplot for standard deviation

                std_before = std_before_array[:,var]
                std_after  = std_after_array[:,var]

                fig, ax = plt.subplots(figsize=(10,4))

                bar_std_before = ax.bar(x_position - width/2, std_before, width, label='before temporal avg')
                bar_std_after  = ax.bar(x_position + width/2, std_after, width, label='after temporal avg')

                title = 'Standard deviation of ' + var_names[var] + ' before and after averaging over a three hour period'
                ax.set_title(title)
                ax.set_xlabel('Station id')
                ax.set_ylabel('Sd')
                ax.set_xticks(x_position)
                ax.set_xticklabels(station_id_list, fontsize=9)
                plt.minorticks_on()
                ax.tick_params(axis='x', which='minor', bottom=False)
                plt.xticks(rotation=90)
                plt.grid(axis = 'y')
                ax.set_axisbelow(True)
                ax.legend()

                fig.tight_layout()

                filename      = 'AMF_temporal-avg_std_1990-2019_' + var_names[var] + '.png'
                filedirectory = FILE_DIRECTORY.replace('npy', 'png')
                filepath      = os.path.join(filedirectory, filename)
                plt.savefig(filepath)


# End of function definition


# FUNCTION TEST - VERSION 7 TEST

min_data_percentage = 80
with_stats          = 'True'

list = Temporal_mean(min_data_percentage, with_stats)
