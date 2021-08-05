import numpy as np
import sys
import datetime
from datetime import timedelta
import fluxnet_classes as fc
import pdb


def Temporal_mean(data_short_period, dates_short_period, t_freq_short, t_freq_long, central_time, min_data_percentage) :


    """

    Calculates the temporal mean for a given time period from the temporal mean of a shorter time period for data of one or more variables.
    
    Parameters :
    
        data_short_period (array)   : Data averaged over the shorter time period. Each column represents one variable.
        
        dates_short_period (array)  : Dates associated with data_short_period.
        
        t_freq_short (int)          : Temporal frequency associated with data_short_period, expressed in seconds.
        
        t_freq_long (int)           : Temporal frequency associated with data_long_period, expressed in seconds.
        
        central_time (float)        : Time about which the temporal mean will be calculated, expressed in hours ranging from 0 to 24 (0 inclusive, 24 exclusive). For example, if 
                                      t_freq_long = 10800 (ie, 3 hours) and we would like to divide a day starting at midnight (00:00 to 03:00, 03:00 to 06:00, etc.), we could
                                      enter 1.5 (the center between 00:00 and 03:00) or 4.5, among other values. 

        min_data_percentage (float) : Minimum amount of data that must be present over the shorter time period to be included in the mean of the longer time period. Expressed
                                      as a percentage from 0 to 100. 
    
    
    Returns :
    
       data_long_period (array)  : Data averaged over the longer time period.
       
       dates_long_period (array) : Dates associated with data_long_period.
       

    Author        : Élise Comeau

    Created       : June 3rd, 2021

    Last modified : August 3rd, 2021


    """


    # Step 1 : Validate the parameters

    if ( data_short_period.shape[0] != dates_short_period.shape[0] ) :

        print('The number of data and date entries do not match. Temporal mean will not be calculated.\n')
        sys.exit(0)

    elif ( ( t_freq_short <= 0 ) or ( t_freq_long <= 0 ) ) :

        print('Temporal frequency is negative. Temporal mean will not be calculated.\n')
        sys.exit(0)

    elif ( t_freq_short >= t_freq_long ) :

        print('Temporal frequencies appear to have been switched. Temporal mean will not be calculated.\n')
        sys.exit(0) 

    elif ( ( central_time < 0 ) or ( central_time >= 24 ) ) :

        print('The central time is out of bounds. Temporal mean will not be calculated.\n')
        sys.exit(0)

    elif ( ( min_data_percentage < 0 ) or ( min_data_percentage > 100 ) ) :

        print('The minimum data percentage is out of bounds. Temporal mean will not be calculated.\n')
        sys.exit(0)

    else :

        print('Data, dates and minimum data percentage are in order. Temporal mean will be calculated.\n')


        # Step 2 : Find the time at which the calculations will begin
	
        # converting the central time to the same format as dates in dates_short_period

        first_time     = dates_short_period[0]
        first_datetime = fc.constants.reference_date + timedelta(seconds=int(first_time)) # the dates represent time deltas, in seconds, since reference_date (ie., January 1st 1971)

        if ( ( central_time - 0.5 * ( t_freq_long / 3600 ) ) >= 0 ) :
            cutoff = central_time - 0.5 * ( t_freq_long / 3600 )      # cutoff represents the transition between two consecutive periods; eg. : the cutoff between 00:00 - 03:00 and 03:00 - 06:00 is 03:00

        else :
            cutoff = central_time + 0.5 * ( t_freq_long / 3600 )

        cutoff_hour   = int(cutoff)
        cutoff_minute = int((cutoff - cutoff_hour) * 60)

        #pdb.set_trace()

        initial_datetime = datetime.datetime(first_datetime.year, first_datetime.month, first_datetime.day, cutoff_hour, cutoff_minute)
        initial_time     = (initial_datetime - fc.constants.reference_date).total_seconds()                                                 # time at which the calculations might begin

        elapsed_time = first_time - initial_time
#        pdb.set_trace()

        # finding the time at which calculations should begin

        while ( elapsed_time < 0 ) :                # initial_time is 'too late'; it must be moved backwards in time
  
            initial_time = initial_time - t_freq_long
            elapsed_time = first_time - initial_time            
#            pdb.set_trace()


        while ( elapsed_time >= t_freq_long ) :   # initial_time is 'too early'; it must be moved forwards in time
             
            initial_time = initial_time + t_freq_long
            elapsed_time = first_time - initial_time

        #pdb.set_trace() 
  

        # Step 3 : Calculate the mean over the longer time period.

        contiguous_data    = []
        contiguous_dates   = []
        total_rows         = data_short_period.shape[0]
        initial_row        = 0                           # row at whihch temporal averaging begins        
        data_per_period    = t_freq_long / t_freq_short  # quantity of data per period, provided all the data is present
        offset             = 0                           # necessary to include the correct amount of rows in the mean calculation 
        #pdb.set_trace()

        for row in range(total_rows) :

            time_difference = dates_short_period[row] - initial_time

            if ( (time_difference >= t_freq_long) or (row == total_rows - 1) ) :

                if ( time_difference < t_freq_long ) :     # if we have not accumulated enough data but we are at the end of data_short_period
                    offset = 1

                number_of_entries = ( row + offset ) - initial_row
                data_percentage   = number_of_entries / data_per_period * 100     # calculate the percentage of data that is present within the current period

                if ( data_percentage >= min_data_percentage ) :

                    contiguous_data.append(np.mean(data_short_period[initial_row:row+offset,:], axis=0))   # data corresponds to the average of each variable (ie, column) for each entry per long temporal frequency
                    contiguous_dates.append(initial_time + t_freq_long / 2)                                # dates correspond to the middle of the period

                initial_time += int(time_difference / t_freq_long) * t_freq_long   # we must find how many t_freq_long have passed since the last initial_time to find the new one
                initial_row   = row

        if ( offset == 0 ) :    # if the last row of data_short_period was excluded from the last period

            data_percentage = 1 / data_per_period * 100            # weight is 1, since only the last row of data was excluded

            if ( data_percentage >= min_data_percentage ) :

                contiguous_data.append(data_short_period[row,:])
                contiguous_dates.append(initial_time + t_freq_long / 2)


        # Step 4 : Return the results from the temporal averaging.

        data_long_period  = np.array(contiguous_data)
        dates_long_period = np.array(contiguous_dates)

        return data_long_period, dates_long_period


# End of function definition
