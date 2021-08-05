import numpy as np
import sys
import glob
import re
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import fluxnet_classes as fc



# CONSTANTS

FILE_DIRECTORY        = '/snow/comeau/FLUXNET_America/1990-2019/npy/' # directory from which the input file is read and to which the output file(s) is/are written
DATA_FILENAME_PREFIX  = 'AMF_data_'                                   # prefix of the data file names to be read
DATES_FILENAME_PREFIX = 'AMF_dates_'                                  # prefix of the dates file names to be read
FILENAME_SUFFIX       = '[!percent].npy'                              # suffix of the data and date file names not to be read

TEMPORAL_MEAN_PERIOD = 3 * 60 * 60             # period over which the temporal mean is done; in this case : 3 hours * 60 mins/h * 60 s/min = 10800 s
TEMPORAL_FREQUENCIES = np.array([1800, 3600])  # accepted temporal frequencies for the input data, in seconds

BAR_WIDTH          = 0.35              # width of bars in the barplots
SHORTER_TIME_LABEL = '30 mins average' # label to be used in the barplots
LONGER_TIME_LABEL  = '3 hrs average'   # other label for the barplots
FIGURE_DIMENSIONS  = (10,6)            # dimensions of the barplots
TITLE_FONT_SIZE    = 9                 # font size for the titles of the barplots
AXIS_FONT_SIZE     = 8                 # font size for the axes label (x and y) of the barplots
LEGEND_FONT_SIZE   = 6                 # font size for the legend of the barplots



def Temporal_mean(min_data_percentage, with_stats) :

    """

    Calculates the average over a given period of time from the average over a shorter period of time (ie, aggregates the data) for a variety of atmospheric variables.    
    Calculates the mean and standard deviation for one or more variables in a data set before and after the temporal averaging, if requested.
    Saves the data and dates of the average over a given period in a file.
    Saves the mean and standard deviations in a file if their calculation was requested.
    Creates and saves a barplot of the means and standard deviations for each variable if these statistics were calculated. 
    Creates and saves a barplot of the number of data entries per station for the given and the shorter period of time.    


    Parameters :

        min_data_percentage (float) : Minimum amount of data required within a period for the mean to be calculated. Expressed as a percentage from 0 to 100.

        with_stats (boolean)        : Option to include the statistics. If 'True', the statistics will be calculated.


    Author        : Élise Comeau

    Created       : June 3rd, 2021

    Last modified : June 11th, 2021


    """


    # Step 1 : Validate the parameters

    with_stats = with_stats.capitalize()

    if ( (min_data_percentage < 0) or (min_data_percentage > 100) ) :

        sys.exit('Minimum data percentage is invalid. Temporal mean will not be calculated.')

    elif ( (with_stats != 'True') and (with_stats != 'False') ) :

        sys.exit('Unable to determine if statistics must be calculated or not. Temporal mean will not be calculated.')

    else :


        # Step 2 : Obtain the list of files to read

        if ( with_stats == 'True' ) : # all the variables necessary for building the bar plot

            station_id_list            = []   # includes station number, country and station name
            mean_before_list           = []
            mean_after_list            = []
            std_before_list            = []
            std_after_list             = []
            nbr_of_entries_before_list = []
            nbr_of_entries_after_list  = []


        data_filenames_pattern  = FILE_DIRECTORY + DATA_FILENAME_PREFIX + '*' + FILENAME_SUFFIX
        dates_filenames_pattern = FILE_DIRECTORY + DATES_FILENAME_PREFIX + '*' + FILENAME_SUFFIX

        data_filenames  = glob.glob(data_filenames_pattern)
        dates_filenames = glob.glob(dates_filenames_pattern)

        nbr_of_stations = len(data_filenames)


        # Step 3 : Read the data and dates from the file

        for station in range(nbr_of_stations) :

            data_before  = np.load(data_filenames[station])
            dates_before = np.load(dates_filenames[station])


            # Step 4 : Extract and validate metadata

            filename = os.path.splitext(os.path.basename(data_filenames[station]))[0]    # produces the filename without the directory path or the file extension
            t_freq   = int(filename.split('_')[ len(filename.split('_')) - 1 ])          # the time frequency corresponds to the last substring of the filename

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

                    nbr_of_entries_before_list.append(data_before.shape[0])


                # Step 6 : Calculate averages for (nearly) contiguous entries

                contiguous_data    = []
                contiguous_weights = []                    # weights of the contiguous data for the calculation of the weighted average (step 7);
                                                           # eg. : if 2 entries were used to calculate the 3 hour average, then the weight of the three hour average is 2
                contiguous_dates   = []
                total_rows         = data_before.shape[0]
                initial_time       = dates_before[0]                # time at which the period begins; we begin counting at the first row
                initial_row        = 0                              # row at which period begins        
                data_per_period    = TEMPORAL_MEAN_PERIOD / t_freq  # quantity of data per period, provided all the data is present
                offset             = 0                              # necessary to include the correct amount of rows in the mean calculation 

                for row in range(total_rows) :

                    time_difference = dates_before[row] - initial_time

                    if ( (time_difference >= TEMPORAL_MEAN_PERIOD) or (row == total_rows - 1) ) :

                        if ( time_difference < TEMPORAL_MEAN_PERIOD ) :     # if we have not accumulated enough data but we are at the end of data_before
                            offset = 1

                        weight          = ( row + offset ) - initial_row
                        data_percentage = weight / data_per_period * 100     # calculate the percentage of data that is present within the current period

                        if ( data_percentage >= min_data_percentage ) :

                            contiguous_data.append(np.mean(data_before[initial_row:row+offset,:], axis=0))   # data corresponds to the average of each variable (ie, column) for each entry per period
                            contiguous_weights.append(weight)                                                # weight is the same for all variables of the same entry
                            contiguous_dates.append(initial_time + TEMPORAL_MEAN_PERIOD / 2)                 # dates correspond to the middle of the period

                        initial_time += int(time_difference / TEMPORAL_MEAN_PERIOD) * TEMPORAL_MEAN_PERIOD   # we must find how many TEMPORAL_MEAN_PERIODs have passed since the last initial_time to find the new one
                        initial_row   = row

                if ( offset == 0 ) :    # if the last row of data_before was excluded from the last period

                    data_percentage = 1 / data_per_period * 100            # weight is 1, since only the last row of data was excluded

                    if ( data_percentage >= min_data_percentage ) :

                        contiguous_data.append(data_before[row,:])
                        contiguous_weights.append(1)
                        contiguous_dates.append(initial_time + TEMPORAL_MEAN_PERIOD / 2)

                data_after  = np.array(contiguous_data)
                dates_after = np.array(contiguous_dates)


                # Step 7 : Calculate the statistics (mean and standard deviation) of the variable(s) after temporal averaging

                if ( with_stats == 'True' ) :

                    mean_after     = np.array(np.average(data_after, axis=0, weights=contiguous_weights))
                    variance_after = np.average((np.vstack(data_after) - mean_after)**2, axis=0, weights=contiguous_weights) 
                    std_after      = np.sqrt(variance_after)

                    mean_after_list.append(mean_after)
                    std_after_list.append(std_after)

                    nbr_of_entries_after_list.append(data_after.shape[0])


                # Step 8 : Write the results of the temporal averaging and the statistics (if applicable) to respective files

                new_suffix = '_' + str(min_data_percentage) + '-percent.npy'
              
                data_filename    = data_filenames[station].replace(str(t_freq), str(TEMPORAL_MEAN_PERIOD))
                data_filename    = data_filename.replace('.npy', new_suffix)
                weights_filename = data_filename.replace('data', 'weights') 
                dates_filename   = data_filename.replace('data', 'dates')

                data_path    = os.path.join(FILE_DIRECTORY, data_filename)
                weights_path = os.path.join(FILE_DIRECTORY, weights_filename) 
                dates_path   = os.path.join(FILE_DIRECTORY, dates_filename)

                np.save(data_path, data_after)
                np.save(weights_path, contiguous_weights)
                np.save(dates_path, dates_after)

                if ( with_stats == 'True' ) :

                    mean_before_array = np.array(mean_before)
                    mean_after_array  = np.array(mean_after)
                    std_before_array  = np.array(std_before)
                    std_after_array   = np.array(std_after)

                    mean_before_filename = data_filenames[station].replace('data', 'mean')
                    mean_after_filename  = data_filename.replace('data', 'mean')
                    std_before_filename  = data_filenames[station].replace('data', 'std')
                    std_after_filename   = data_filename.replace('data', 'std')  

                    np.save(mean_before_filename, mean_before_array)
                    np.save(mean_after_filename, mean_after_array)
                    np.save(std_before_filename, std_before_array)
                    np.save(std_after_filename, std_after_array)


        # Step 9 : Create and save plot for number of data entries

        nbr_of_entries_before_array        = np.array(nbr_of_entries_before_list)
        nbr_of_entries_after_array         = np.array(nbr_of_entries_after_list)
        nbr_of_entries_relative_difference = abs( ( nbr_of_entries_after_array - nbr_of_entries_before_array ) / nbr_of_entries_before_array ) * 100

        x_position = np.arange(len(station_id_list))

        plt.figure()        
        fig, ax = plt.subplots(2, figsize=FIGURE_DIMENSIONS)

        ax[0].bar(x_position - BAR_WIDTH/2, nbr_of_entries_before_array, BAR_WIDTH, label=SHORTER_TIME_LABEL)
        ax[0].bar(x_position + BAR_WIDTH/2, nbr_of_entries_after_array, BAR_WIDTH, label=LONGER_TIME_LABEL)

        ax[1].scatter(x_position, nbr_of_entries_relative_difference, color='black')

        plot_title     = 'Number of data entries per site of measurement according to averaging period and site of measurement (minimum data percentage = ' + str(min_data_percentage) + '%)'
        x_axis_title   = 'Site of measurement'
        y_axis_title_0 = 'Number of data entries\nper site of measurement'
        y_axis_title_1 = 'Relative difference\nof number of data entries\nper site of measurement (%)'

        fig.suptitle(plot_title, fontsize=TITLE_FONT_SIZE, fontweight='bold')
        ax[0].set_ylabel(y_axis_title_0, fontsize=AXIS_FONT_SIZE, fontweight='bold')
        ax[1].set_xlabel(x_axis_title, fontsize=AXIS_FONT_SIZE, fontweight='bold')
        ax[1].set_ylabel(y_axis_title_1, fontsize=AXIS_FONT_SIZE, fontweight='bold')

        ax[0].legend(fontsize=LEGEND_FONT_SIZE)

        ax[0].set_xticks(x_position)
        ax[0].yaxis.set_minor_locator(tck.AutoMinorLocator())
        ax[0].tick_params(labelsize=AXIS_FONT_SIZE)
        ax[1].set_xticks(x_position)
        ax[1].yaxis.set_minor_locator(tck.AutoMinorLocator())
        ax[1].tick_params(labelsize=AXIS_FONT_SIZE)

        ax[0].set_xticklabels([])
        ax[1].set_xticklabels(station_id_list, fontsize=AXIS_FONT_SIZE, rotation=90)

        ax[0].yaxis.grid()
        ax[0].set_axisbelow(True)
        ax[1].yaxis.grid()
        ax[1].set_axisbelow(True)

        fig.tight_layout()

        filename      = 'AMF_nbr-of-entries_1990-2019_' + str(t_freq) + '-' + str(TEMPORAL_MEAN_PERIOD) + '_' + str(min_data_percentage) + '-percent.png'
        filedirectory = FILE_DIRECTORY.replace('npy', 'png')
        filepath      = os.path.join(filedirectory, filename)
        plt.savefig(filepath)
       

        # Step 10 : Create and save plots for statistics

        if ( with_stats == 'True' ) :

            mean_before_array = np.array(mean_before_list)
            mean_after_array  = np.array(mean_after_list)
            std_before_array  = np.array(std_before_list)
            std_after_array   = np.array(std_after_list)

            nbr_of_vars     = len(var_names)
            nbr_of_stations = len(station_id_list)
            station_nbrs    = range(nbr_of_stations)

            for var in range(nbr_of_vars) :

                unit = fc.variables.units[var_names[var]]

                # plot for mean

                mean_before              = mean_before_array[:,var]
                mean_after               = mean_after_array[:,var] 
                mean_relative_difference = abs( ( mean_after - mean_before ) / mean_before ) * 100

                fig, ax = plt.subplots(2, figsize=FIGURE_DIMENSIONS)

                ax[0].bar(x_position - BAR_WIDTH/2, mean_before, BAR_WIDTH, label=SHORTER_TIME_LABEL)
                ax[0].bar(x_position + BAR_WIDTH/2, mean_after, BAR_WIDTH, label=LONGER_TIME_LABEL)

                ax[1].scatter(x_position, mean_relative_difference, color='black')

                plot_title     = 'Mean of ' + var_names[var] + ' according to averaging period and site of measurement (minimum data percentage = ' + str(min_data_percentage) + '%)'
                y_axis_title_0 = 'Mean of ' + var_names[var] + ' (' + unit + ')'
                y_axis_title_1 = 'Relative difference\nof mean of ' + var_names[var] + ' (%)'

                fig.suptitle(plot_title, fontsize=TITLE_FONT_SIZE, fontweight='bold')
                ax[0].set_ylabel(y_axis_title_0, fontsize=AXIS_FONT_SIZE, fontweight='bold')
                ax[1].set_xlabel(x_axis_title, fontsize=AXIS_FONT_SIZE, fontweight='bold')
                ax[1].set_ylabel(y_axis_title_1, fontsize=AXIS_FONT_SIZE, fontweight='bold')

                ax[0].legend(fontsize=LEGEND_FONT_SIZE)

                ax[0].set_xticks(x_position)
                ax[0].yaxis.set_minor_locator(tck.AutoMinorLocator())
                ax[0].tick_params(labelsize=AXIS_FONT_SIZE)
                ax[1].set_xticks(x_position)
                ax[1].yaxis.set_minor_locator(tck.AutoMinorLocator())
                ax[1].tick_params(labelsize=AXIS_FONT_SIZE)

                ax[0].set_xticklabels([])
                ax[1].set_xticklabels(station_id_list, fontsize=AXIS_FONT_SIZE, rotation=90)

                ax[0].yaxis.grid()
                ax[0].set_axisbelow(True)
                ax[1].yaxis.grid()
                ax[1].set_axisbelow(True) 

                fig.tight_layout()

                filename      = 'AMF_mean_1990-2019_' + var_names[var] +'_' +  str(t_freq) + '-' + str(TEMPORAL_MEAN_PERIOD) + '_' + str(min_data_percentage) + '-percent.png'
                filedirectory = FILE_DIRECTORY.replace('npy', 'png') 
                filepath      = os.path.join(filedirectory, filename)  
                plt.savefig(filepath)


                # plot for standard deviation

                std_before              = std_before_array[:,var]
                std_after               = std_after_array[:,var]
                std_relative_difference = abs( ( std_after - std_before ) /std_before ) * 100

                fig, ax = plt.subplots(2, figsize=FIGURE_DIMENSIONS)

                ax[0].bar(x_position - BAR_WIDTH/2, std_before, BAR_WIDTH, label=SHORTER_TIME_LABEL)
                ax[0].bar(x_position + BAR_WIDTH/2, std_after, BAR_WIDTH, label=LONGER_TIME_LABEL)

                ax[1].scatter(x_position, std_relative_difference, color='black')

                plot_title     = 'Standard deviation of ' + var_names[var] + ' according to averaging period and site of measurement (minimum data percentage = ' + str(min_data_percentage) + '%)'
                y_axis_title_0 = 'Standard deviation of ' + var_names[var] + ' (' + unit + ')'
                y_axis_title_1 = 'Relative difference\nof standard deviation of ' + var_names[var] + ' (%)'

                fig.suptitle(plot_title, fontsize=TITLE_FONT_SIZE, fontweight='bold')
                ax[0].set_ylabel(y_axis_title_0, fontsize=AXIS_FONT_SIZE, fontweight='bold')
                ax[1].set_xlabel(x_axis_title, fontsize=AXIS_FONT_SIZE, fontweight='bold')
                ax[1].set_ylabel(y_axis_title_1, fontsize=AXIS_FONT_SIZE, fontweight='bold')

                ax[0].legend(fontsize=LEGEND_FONT_SIZE)

                ax[0].set_xticks(x_position)
                ax[0].yaxis.set_minor_locator(tck.AutoMinorLocator())
                ax[0].tick_params(labelsize=AXIS_FONT_SIZE)
                ax[1].set_xticks(x_position)
                ax[1].yaxis.set_minor_locator(tck.AutoMinorLocator())
                ax[1].tick_params(labelsize=AXIS_FONT_SIZE)

                ax[0].set_xticklabels([])
                ax[1].set_xticklabels(station_id_list, fontsize=AXIS_FONT_SIZE, rotation=90)

                ax[0].yaxis.grid()
                ax[0].set_axisbelow(True)
                ax[1].yaxis.grid()
                ax[1].set_axisbelow(True)

                fig.tight_layout()

                filename      = 'AMF_std_1990-2019_' + var_names[var] + '_' + str(t_freq) + '-' + str(TEMPORAL_MEAN_PERIOD) + '_' + str(min_data_percentage) + '-percent.png'
                filedirectory = FILE_DIRECTORY.replace('npy', 'png')
                filepath      = os.path.join(filedirectory, filename)
                plt.savefig(filepath)


# End of function definition



# FUNCTION TEST - VERSION 7 TEST

min_data_percentage = 0
with_stats          = 'True'

Temporal_mean(min_data_percentage, with_stats)
