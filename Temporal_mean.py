import numpy as np
import sys

TEMPORAL_MEAN_PERIOD = 3 * 60 * 60          # period over which the temporal mean is done; in this case : 3 hours * 60 mins/h * 60 s/min = 10800 s
TEMPORAL_FREQUENCIES = np.array([30, 60])   # accepted temporal frequencies for the input data, in minutes


def Temporal_mean (data, dates, t_freq, min_data_percentage):

    """

    Calculates the average over a given period of time from the average over a shorter period of time for a variety of atmospheric variables.


    Parameters:

        data (array)                : Data averaged over the shorter time period.

        dates (array)               : Dates associated with shorter time period averages. Hence, the dates and data arrays must have the same number of rows.   

        t_freq (int)                : Temporal frequency of the dates in minutes. Must match one of the accepted temporal frequencies.

        min_data_percentage (float) : Minimum amount of data required within a period for the mean to be calculated. Expressed as a percentage from 0 to 100.


    Returns:

        temporal_mean_data (array)  : Average of the variable(s) in data over the given period.

        temporal_mean_dates (array) : Dates corresponding with the averaged data.


    Author        : Élise Comeau

    Created       : May 31st, 2021

    Last modified : June 3rd, 2021


    """


    # Step 1 : Validate the parameters

    if ( t_freq not in TEMPORAL_FREQUENCIES ) :

        sys.exit('Temporal frequency is not valid. Temporal mean will not be calculated.')

    elif ( data.shape[0] != dates.shape[0] ) :

        sys.exit('The number of data and date entries do not match. Temporal mean will not be calculated.')

    else :


        # Step 2 : Calculate averages for (nearly) contiguous entries

        print('Data, dates and temporal frequency are in order. Temporal mean will be calculated.\n')

        time_delta       = t_freq * 60                           # convert to seconds
        contiguous_data  = []
        contiguous_dates = []
        total_rows       = data.shape[0]
        initial_time     = dates[0]                              # time at which the period begins; we begin counting at the first row
        initial_row      = 0                                     # row at which period begins        
        data_per_period  = TEMPORAL_MEAN_PERIOD / time_delta     # quantity of data per period, provided all the data is present
        offset           = 0                                     # necessary to include the correct amount of rows in the mean calculation 

        print('time_delta = ' + str(time_delta))
        print('total_rows = ' + str(total_rows))
        print('initial_time = ' + str(initial_time))
        print('data_per_period = ' + str(data_per_period) + '\n')

        for row in range(total_rows) :

            time_difference = dates[row] - initial_time
            print('For row ' + str(row) + ', the time difference is : ' + str(time_difference))
            print('The initial time is : ' + str(initial_time))

            if ( (time_difference >= TEMPORAL_MEAN_PERIOD) or (row == total_rows - 1) ) :

                if ( row == total_rows - 1 ) :
                    offset = 1

                data_percentage = (row - initial_row + offset) / data_per_period * 100     # calculate the percentage of data that is present within the current period
                print('data_percentage = ' + str(data_percentage))

                if ( data_percentage >= min_data_percentage ) :

                    contiguous_data.append(np.mean(data[initial_row:row+offset,:], axis=0))  # data corresponds to the average of each variable (ie, column) for each entry per period
                    contiguous_dates.append(initial_time + TEMPORAL_MEAN_PERIOD / 2)  # dates correspond to the middle of the period

                initial_time += TEMPORAL_MEAN_PERIOD
                initial_row   = row


    # Step 3 : Return the averaged data and dates

    temporal_mean_data  = np.array(contiguous_data)
    temporal_mean_dates = np.array(contiguous_dates)

    return temporal_mean_data, temporal_mean_dates;


# End of function definition


data_1  = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9], [10, 11]])
dates_1 = np.array([0, 3600, 7200, 10800, 14400, 18000])

t_freq = 60
min_data_percentage = 100

avg_data, avg_dates = Temporal_mean(data_1, dates_1, t_freq, min_data_percentage)
