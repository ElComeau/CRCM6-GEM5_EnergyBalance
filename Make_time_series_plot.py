import fluxnet_classes as fc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import locale
import Epoch_to_datetime as etd
import Get_datetime_index as gdi
import pdb


def Make_time_series_plot(dates_arrays_list, data_arrays_list, labels_list, var_name, filepath) :

    """
    Creates a plot showing the values of different sets of data according to their respective dates.


    Parameters :

        dates_arrays_list (list) : List of date arrays associated with data.

        data_arrays_list (list)  : List of data arrays to plot.

        labels_list (list)       : List of labels to use for the plot. Each label is associated with a data array.  

        var_name (string)        : Name of the variable to be plotted (eg. 'G').

        filepath (string)        : Filepath used to save the plot.


    Author        : Élise Comeau

    Created       : June 15th 2021

    Last modified : August 4th 2021 

    """



    # Step 1 : Convert dates to datetime format

    datetime_arrays_list = []

    for dates_array in dates_arrays_list :

        datetime_list  = etd.epoch_to_datetime(dates_array, fc.constants.reference_date)
        datetime_array = np.asarray(datetime_list)

        datetime_arrays_list.append(datetime_array)
        #pdb.set_trace()


    # Step 2 : Initialize plot paramaters

    counter         = 0

    fig_size_width  = 22
    fig_size_height = 6

    marker_types    = ['x', '^', 'o', 's', 'd', '*', 'p']
    alpha_value     = 0.7

    datetime_format  = '%H:%M %d/%m/%y'
    loc              = 'en_CA'

    var_unit = fc.variables.units[var_name]
    x_label  = 'Local Time [hh:mm dd/mm/yy]'
    y_label  = 'Value of ' + var_name + ' [' + var_unit + ']'


    # Step 3 : Add dates and data to plot

    fig = plt.figure(figsize=(fig_size_width, fig_size_height))
    ax  = fig.add_subplot(1,1,1)

    locale.setlocale(locale.LC_TIME, loc)
    ax.xaxis.set_major_formatter(mdates.DateFormatter(datetime_format))

    for datetime_array, data_array in zip(datetime_arrays_list, data_arrays_list) :
   
        if ( counter == 0 ) :

            start_datetime_index = 0
            end_datetime_index   = 144

            specific_start_datetime = datetime_array[start_datetime_index]
            specific_end_datetime   = datetime_array[end_datetime_index] 

            line_style = 'None'

        else :

            start_datetime_index = gdi.Get_datetime_index(datetime_array, specific_start_datetime)
            end_datetime_index   = gdi.Get_datetime_index(datetime_array, specific_end_datetime) + 1

            line_style  = 'solid'

        marker_type = marker_types[counter]
        plt.plot(datetime_array[start_datetime_index:end_datetime_index], data_array[start_datetime_index:end_datetime_index], label=labels_list[counter], marker=marker_type, linestyle=line_style, alpha=alpha_value)
        counter = counter + 1


    # Step 4 : Add identifiers to plot

    plt.xlabel(x_label, fontweight='bold')
    plt.ylabel(y_label, fontweight='bold')

    plt.legend()

    plt.savefig(filepath, bbox_inches="tight")
