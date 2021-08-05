import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tck


def Make_comparison_plot(station_numbers, station_names, data_1, data_2, plot_title, y_axis_label, legend_label_1, legend_label_2, filepath) :
  
    """
      
    Creates a plot comparing the values of two sets of data according to the station.
    Each plot contains two subplots. The first is a grouped barplot representing the values of the two data sets.
    The second is a scatter plot representing the relative difference between the two data sets.

      
    Parameters :
      
        station_numbers (array) : Station numbers of the stations to be plotted.
          
        station_names (array)   : Station names of the stations to be plotted.
          
        data_1 (array)          : First set of data to compare.
          
        data_2 (array)          : Second set of data to compare.
          
        plot_title (string)     : Title of the plot.
         
        y_axis_label (sring)    : Label used for the y axis (ie, what the data represents).
          
        label_1 (string)        : Label used in legend of barplot for data_1.
          
        label_2 (string)        : Label used in legend of barplot for data_2.          

        filename (string)       : Path of file where plot is saved.


    Author        : Élise Comeau

    Created       : June 3rd, 2021

    Last modified : July 19th, 2021

    """


    # Step 1 : Validate the parameters

    if ( station_numbers.shape != station_names.shape ) :

        print('There is a mismatch between the number of station numbers and station names. Comparison plots cannot be produced.\n')
        sys.exit(0)

    elif ( data_1.shape != data_2.shape ) :

        print('There is a mismatch between the amount of data in the comparison sets. Comparison plots cannot be produced.\n')
        sys.exit(0)

    else :


        # Step 2 : Prepare the plots

        data_relative_difference = abs( ( data_1 - data_2 ) / data_1 ) * 100

        bar_width         = 0.35    # width of bars in the barplots
        figure_dimensions = (10,6)
        title_font_size   = 9 
        axis_font_size    = 7
        legend_font_size  = 6

        x_axis_label             = 'Site of measurement'
        y_axis_label_barplot     = y_axis_label
        y_axis_label_scatterplot = 'Relative difference of\n' + y_axis_label + ' (%)'

        number_of_stations = station_numbers.shape[0]
        station_ids        = []

        for index in range(number_of_stations) :

            station_ids.append(str(station_numbers[index]) + '_' + str(station_names[index])) 

        x_position = np.arange(len(station_ids))


        # Step 3 : Create the barplot

        plt.figure()        
        fig, ax = plt.subplots(2, figsize=figure_dimensions)

        ax[0].bar(x_position - bar_width/2, data_1, bar_width, label=legend_label_1)
        ax[0].bar(x_position + bar_width/2, data_2, bar_width, label=legend_label_2)

        fig.suptitle(plot_title, fontsize=title_font_size, fontweight='bold')
        ax[0].set_ylabel(y_axis_label_barplot, fontsize=axis_font_size, fontweight='bold')

        ax[0].legend(fontsize=legend_font_size)

        ax[0].set_xticks(x_position)
        ax[0].yaxis.set_minor_locator(tck.AutoMinorLocator())
        ax[0].tick_params(labelsize=axis_font_size)

        ax[0].set_xticklabels([])

        ax[0].yaxis.grid()
        ax[0].set_axisbelow(True)


        # Step 4 : Create the scatter plot

        ax[1].scatter(x_position, data_relative_difference, color='black')
        
        ax[1].set_xlabel(x_axis_label, fontsize=axis_font_size, fontweight='bold')
        ax[1].set_ylabel(y_axis_label_scatterplot, fontsize=axis_font_size, fontweight='bold')

        ax[1].set_xticks(x_position)
        ax[1].yaxis.set_minor_locator(tck.AutoMinorLocator())
        ax[1].tick_params(labelsize=axis_font_size)

        ax[1].set_xticklabels(station_ids, fontsize=axis_font_size, rotation=90)

        ax[1].yaxis.grid()
        ax[1].set_axisbelow(True)

        fig.tight_layout()
        plt.savefig(filepath)


# End of function definition
