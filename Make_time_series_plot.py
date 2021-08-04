import fluxnet_classes as fc
import numpy as np
import matplotlib.pyplot as plt
import pdb


def Compare_min_data_percentage(data_short_period, dates_short_period, t_freq_short, t_freq_long, central_time, min_data_percentages, time_length, var_name, var_index, station_id) :

    """

    Creates a plot showing the values of different sets of data according to their respective dates, temporal frequency and minimum data percentage for a single station.


    Parameters :

        data_short_period (array)    : Data used for the plot. Since the data will be averaged over a longer period, enter the data with the shortest averaging period that will be presented in the plot.

        dates_short_period (array)   : Dates associated with data.

        t_freq_short (int)           : Temporal frequency of data in hours.

        t_freq_long (int)            : Temporal frequency of the data averaged over the longer period in hours.

        central_time (float)         : Time about which the temporal mean will be calculated, expressed in hours ranging from 0 to 24 (0 inclusive, 24 exclusive). For example, if 
                                       t_freq_long = 10800 (ie, 3 hours) and we would like to divide a day starting at midnight (00:00 to 03:00, 03:00 to 06:00, etc.), we could
                                       enter 1.5 (the center between 00:00 and 03:00) or 4.5, among other values. 

        min_data_percentages (array) : Minimum data percentage(s) that will be presented in the plot.

        time_length (float)          : Amount of time to be presented in the plot in hours.

        var_name (string)            : Name of the variable to be plotted (eg. 'G').

        var_index (int)              : Index of the variable to be plotted (ie, the index of the column corresponding to the variable to be plotted). 

        station_id (string)          : Identification of the station whose data will be plotted. This can include the station number, station name, etc. 



    Author        : Élise Comeau

    Created       : June 15th 2021

    Last modified : June 18th 2021 

    """


    # Step 1 : Obtain dates to plot

    initial_date = dates_short_period[0]
    final_date   = initial_date + time_length * 3600   # 3600 to convert hours to seconds
    time_step    = t_freq_short * 3600

    ref_times = np.arange(initial_date, final_date, time_step)
    last_row  = ref_times.shape[0]                             # last row that will be plotted in data

#    pdb.set_trace()


    # Step 2 : Generate data and dates for the long period(s)

    data_list  = [ data_short_period ]
    dates_list = [ dates_short_period ]

    legend      = str(t_freq_short) + ' hr avg' 
    legend_list = [ legend ] 

    for min_data_percentage in min_data_percentages :

        data_long_period, dates_long_period = fc.Temporal_mean(data_short_period, dates_short_period, t_freq_short * 3600, t_freq_long * 3600, central_time, min_data_percentage)

        data_list.append(data_long_period)
        dates_list.append(dates_long_period)

        legend = str(t_freq_long) + ' hr avg (min. data percentage = ' + str(min_data_percentage) + '%)'
        legend_list.append(legend)

#        pdb.set_trace()

#    pdb.set_trace()


    # Step 3 : Add missing values

#    index = 0

    for data, dates in zip(data_list, dates_list) :

        for time in ref_times :

            if ( time not in dates ) :

#                print( str(time) + ' not found.')

                insert_index = np.amin(np.where(dates > time))
                dates        = np.insert(dates, insert_index, time)
                data         = np.insert(data, insert_index, fc.constants.missing_value, axis=0)

                pdb.set_trace()

#                if ( index != 0 ) :
#                    pdb.set_trace()

#            else :

#                print ( str(time) + ' found.') 

        data = np.ma.masked_where(data == fc.constants.missing_value, data)


        # Step 4 : Add data, dates to plot

        plt.plot(dates[:last_row], data[:last_row, var_index], linestyle=None, marker='o')
#        plt.plot(dates[:last_row], data[:last_row, var_index], linestyle=None, marker='+')
#            pdb.set_trace()

#        index = index + 1

#        pdb.set_trace()	


    # Step 5 : Add labels to plot

    var_unit = fc.variables.units[var_name]

    title = 'Value of ' + var_name + ' according to time, averaging period and minimum data percentage (station = ' + station_id + ')'
    x_label = 'Time (s)'
    y_label = 'Value of ' + var_name + ' (' + var_unit + ')' 

    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel(x_label, fontsize=12, fontweight='bold')
    plt.ylabel(y_label, fontsize=12, fontweight='bold') 
    plt.legend(legend_list)

    pdb.set_trace()
    plt.show()
 


# End of function definition
