import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import Calculate_stats_v2 as cs
import pdb


def Make_comparison_plot(station_ids, data_list_1, data_list_2, y_axis_label_1, y_axis_label_2, legend_label_list_1, legend_label_list_2, filepath) :
  
    """
      
    Creates a plot comparing the values of two or more sets of data according to the station.
    The plot contains two subplots, both of which are barplots, and their medians, represented by a horizontal line.

      
    Parameters :
      
        station_ids (list)         : Station ids of the stations to be plotted.
          
        data_list_1 (list)         : List of sets of data to be plotted in the first subplot.

        data_list_2 (list)         : List of sets of data to be plotted in the second subplot.

        y_axis_label_1 (string)    : Label used for the y axis in the first subplot (ie, what the data represents).

        y_axis_label_2 (string)    : Label used for the y axis in the second subplot.
          
        legend_label_list_1 (list) : List of labels used in the legend of the first subplot.
          
        legend_label_list_2 (list) : List of labels used in the legend of the second subplot.          

        filepath (string)          : Path of file where plot is saved.


    Author        : Élise Comeau

    Created       : June 3rd, 2021

    Last modified : August 4th, 2021

    """


    # Step 1 : Validate the parameters

    #pdb.set_trace()
    nbr_of_stations = len(station_ids)


    data_list_1_length_is_valid = 'True'
    data_list_2_length_is_valid = 'True'

    for data_1 in data_list_1 :

        if ( nbr_of_stations != len(data_1) ) :
            data_list_1_length_is_valid = 'False'

    for data_2 in data_list_2 :

        if ( nbr_of_stations != len(data_2) ) :
            data_list_2_length_is_valid = 'False'

    if ( data_list_1_length_is_valid == 'False' ) :

        print('There is a mismatch between the number of stations and the amount of data for the first subplot. Comparison plots cannot be produced.\n')
        pdb.set_trace()
        sys.exit(0)

    elif ( data_list_2_length_is_valid == 'False' ) :

        print('There is a mismatch between the number of stations and the amount of data for the second subplot. Comparison plots cannot be produced.\n')
        pdb.set_trace()
        sys.exit(0)

    else :


        # Step 2 : Obtain the median of each list of sets of data

        stats_name = ['MEDIAN']

        medians_list_1 = []
        medians_list_2 = []

        nbr_of_rows         = len(station_ids)
        nbr_of_sets_of_data = len(data_list_1)

        for data_set in data_list_1 :

            data_set_array = np.asarray(data_set)
            #nbr_of_rows    = data_set_array.shape[0]

            median       = cs.Calculate_stats(stats_name, data_set_array)[0]
            median_array = np.full((2,), median) 

            medians_list_1.append(median_array)

        for data_set in data_list_2 :

            data_set_array = np.asarray(data_set)
            #nbr_of_rows    = data_set_array.shape[0]

            median       = cs.Calculate_stats(stats_name, data_set_array)[0]
            median_array = np.full((2,), median)

            medians_list_2.append(median_array)


        # Step 3 : Prepare the plots

        figure_dimensions = (18 , 10)
        bar_width         = 0.7 / nbr_of_sets_of_data    # width of bars in the barplots

        x_axis_label = 'Site of measurement'

        axis_font_size   = 12
        legend_font_size = 10

        x_position = np.arange(nbr_of_rows)

        median_start_position = x_position[0] - 3 * bar_width
        median_end_position   = x_position[ len(x_position) - 1 ] + 3 * bar_width

        median_position = [ median_start_position, median_end_position ]

        # Step 4 : Create first subplot

        plt.figure()        
        fig, ax = plt.subplots(2, figsize=figure_dimensions)
            
        for index in range(nbr_of_sets_of_data) :

            bar_position = x_position + (index - 2) * bar_width

            ax[0].bar(bar_position, data_list_1[index], bar_width, label=legend_label_list_1[index])
            ax[0].plot(median_position, medians_list_1[index])

        ax[0].set_ylabel(y_axis_label_1, fontsize=axis_font_size, fontweight='bold')
        ax[0].legend(fontsize=legend_font_size)
        ax[0].set_xticks(x_position)
        ax[0].set_xlim(-0.7, len(x_position))
        ax[0].tick_params(labelsize=axis_font_size)
        ax[0].set_xticklabels([])
        ax[0].yaxis.grid()
        ax[0].set_axisbelow(True)
        ax[0].set_title('a)',  loc='left')


        # Step 5 : Create second subplot

        for index in range(nbr_of_sets_of_data) :

            bar_position = x_position +	(index - 2) * bar_width

            ax[1].bar(bar_position, data_list_2[index], bar_width, label=legend_label_list_2[index])
            ax[1].plot(median_position, medians_list_2[index], label=legend_label_list_2[index])

        ax[1].set_xlabel(x_axis_label, fontsize=axis_font_size, fontweight='bold')
        ax[1].set_ylabel(y_axis_label_2, fontsize=axis_font_size, fontweight='bold')
        ax[1].set_xticks(x_position)
        ax[1].set_xlim(-0.7, len(x_position))
        ax[1].tick_params(labelsize=axis_font_size)
        ax[1].set_xticklabels(station_ids, fontsize=axis_font_size, rotation=90)
        ax[1].yaxis.grid()
        ax[1].set_axisbelow(True)
        ax[1].set_title('b)', loc='left')

        fig.tight_layout()
        plt.savefig(filepath, bbox_inches="tight")
