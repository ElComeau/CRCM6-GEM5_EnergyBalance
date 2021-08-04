import fluxnet_classes as fc
import numpy as np
import matplotlib.pyplot as plt



""" CONSTANTS """

T_FREQ_SHORT = 30 * 60        # 30 mins * 60 mins/s = 180 s
T_FREQ_LONG  = 3 * 60 * 60    # 3 hrs * 60 mins/hr * 60 s/min = 10800 s 

ROW_NBR_START = 0    # first entry that is plotted   
ROW_NBR_STOP  = 20   # last entry that is plotted
COLUMN_NBR   = 0     # column 0 corresponds to variable G; choice is arbitrary

STATION_ID = '001_CA-DBB'     # station number, country, station name
VAR_NAME   = 'G'
VAR_UNIT   = '(W * m^(-2))'



def Compare_min_data_percentage(data_short_period, dates_short_period, min_data_percentages) :

    """

    Creates a plot showing the values of different sets of data according to their respective dates, temporal frequency and minimum data percentage used to generate the data when applicable.


    Parameters :

        data (array)                 : Data used for the plot. Since the data will be averaged over a longer period, enter the data with the shortest averaging period that will be presented in the plot.

        dates (array)                : Dates associated with data.

        min_data_percentages (array) : The minimum data percentage(s) that will be presented in the plot.


    Author        : Élise Comeau

    Created       : June 15th 2021

    Last modified : June 16th 2021 

    """



    # Step 1 : Plot the data and dates for the short period
    
    legends_list = []

    plt.plot(dates_short_period[ROW_NBR_START:ROW_NBR_STOP], data_short_period[:20, COLUMN_NBR], linestyle=None, marker='+')

    legend_label_short_period =	str(T_FREQ_SHORT / 60) + ' mins avg'
    legends_list.append(legend_label_short_period)


    # Step 2 : Plot the data and dates for the long period(s)

    for min_data_percentage in min_data_percentages :

        data_long_period, dates_long_period = fc.Temporal_mean(data_short_period, dates_short_period, T_FREQ_SHORT, T_FREQ_LONG, min_data_percentage)

        plt.plot(dates_long_period[:20], data_short_period[ROW_NBR_START:ROW_NBR_STOP, COLUMN_NBR], linestyle=None, marker='+')

        legend_label_long_period = str(T_FREQ_LONG / (60 * 60)) + ' hrs avg (min. data percentage = ' + str(min_data_percentage) + '%)'
        legends_list.append(legend_label_long_period)


    # Step 3 : Add labels to plot

    title = 'Value of ' + VAR_NAME + ' according to time, averaging period and minimum data percentage (station = ' + STATION_ID + ')'
    x_label = 'Time (s)'
    y_label = 'Value of ' + VAR_NAME + ' ' + VAR_UNIT

    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel(x_label, fontsize=12, fontweight='bold')
    plt.ylabel(y_label, fontsize=12, fontweight='bold') 
    plt.legend(legends_list)

    plt.show()
 


# End of function definition
