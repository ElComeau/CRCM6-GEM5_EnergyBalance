import sys
import numpy as np
import matplotlib.pyplot as plt
import Calculate_stats as cs
import pdb


def Make_comparative_bar_plot(data_x_list, data_y_list_1, data_y_list_2, x_axis_label, y_axis_label_1, y_axis_label_2, legend_label_list_1, legend_label_list_2, filepath) :
  
    """
      
    Creates a plot comparing the values of two or more sets of data who share the same x values.
    The plot contains two subplots, both of which are barplots, and their medians, represented by a horizontal line.

      
    Parameters :
      
        data_x_list (list)         : List of x values of data.
          
        data_y_list_1 (list)       : List of sets of y values to be plotted in the first subplot.

        data_y_list_2 (list)       : List of sets of y values to be plotted in the second subplot.

        x_axis_label (string)      : Label used for the x axis. Applies to both subplots.

        y_axis_label_1 (string)    : Label used for the y axis in the first subplot (ie, what the data represents).

        y_axis_label_2 (string)    : Label used for the y axis in the second subplot.
          
        legend_label_list_1 (list) : List of labels used in the legend of the first subplot.
          
        legend_label_list_2 (list) : List of labels used in the legend of the second subplot.          

        filepath (string)          : Path of file where plot is saved.


    Author        : Élise Comeau

    Created       : June 3rd, 2021

    Last modified : August 5th, 2021

    """


    # Step 1 : Validate the parameters

    data_y_list_1_length_is_valid = 'True'
    data_y_list_2_length_is_valid = 'True'

    for data_y_1 in data_y_list_1 :

        if ( len(data_x_list) != len(data_y_1) ) :
            data_y_list_1_length_is_valid = 'False'

    for data_y_2 in data_y_list_2 :

        if ( len(data_x_list) != len(data_y_2) ) :
            data_y_list_2_length_is_valid = 'False'

    if ( data_y_list_1_length_is_valid == 'False' ) :

        print('There is a mismatch between the amount of x and y values for the first subplot. Comparison plot cannot be produced.\n')
        sys.exit(0)

    elif ( data_y_list_2_length_is_valid == 'False' ) :

        print('There is a mismatch between the amount of x and y values for the second subplot. Comparison plot cannot be produced.\n')
        sys.exit(0)

    else :


        # Step 2 : Obtain the median of each list of sets of data

        stats_name = ['MEDIAN']

        medians_list_1 = []
        medians_list_2 = []

        nbr_of_rows         = len(data_x_list)
        nbr_of_sets_of_data = len(data_y_list_1)

        for data_set in data_y_list_1 :

            data_set_array = np.asarray(data_set)

            median       = cs.Calculate_stats(stats_name, data_set_array)[0]
            median_array = np.full((2,), median) 

            medians_list_1.append(median_array)

        for data_set in data_y_list_2 :

            data_set_array = np.asarray(data_set)

            median       = cs.Calculate_stats(stats_name, data_set_array)[0]
            median_array = np.full((2,), median)

            medians_list_2.append(median_array)


        # Step 3 : Prepare the plots

        figure_dimensions = (18 , 10)

        bar_width = 0.7 / nbr_of_sets_of_data    # width of bars in the barplots

        x_position            = np.arange(nbr_of_rows)
        median_start_position = x_position[0] - 3 * bar_width
        median_end_position   = x_position[ len(x_position) - 1 ] + 3 * bar_width
        median_position       = [ median_start_position, median_end_position ]

        axis_font_size   = 12
        legend_font_size = 10


        # Step 4 : Create first subplot

        plt.figure()        
        fig, ax = plt.subplots(2, figsize=figure_dimensions)
            
        for index in range(nbr_of_sets_of_data) :

            bar_position = x_position + (index - 2) * bar_width

            ax[0].bar(bar_position, data_y_list_1[index], bar_width, label=legend_label_list_1[index])
            ax[0].plot(median_position, medians_list_1[index])

        ax[0].set_xlim(-0.7, len(x_position))

        ax[0].set_xticks(x_position)
        ax[0].set_xticklabels([])
        ax[0].tick_params(labelsize=axis_font_size)
        ax[0].yaxis.grid()
        ax[0].set_ylabel(y_axis_label_1, fontsize=axis_font_size, fontweight='bold')
        ax[0].set_axisbelow(True)

        ax[0].legend(fontsize=legend_font_size)
        ax[0].set_title('a)',  loc='left')


        # Step 5 : Create second subplot

        for index in range(nbr_of_sets_of_data) :

            bar_position = x_position +	(index - 2) * bar_width

            ax[1].bar(bar_position, data_y_list_2[index], bar_width, label=legend_label_list_2[index])
            ax[1].plot(median_position, medians_list_2[index], label=legend_label_list_2[index])

        ax[1].set_xlim(-0.7, len(x_position))

        ax[1].set_xticks(x_position)
        ax[1].set_xticklabels(data_x_list, fontsize=axis_font_size, rotation=90)
        ax[1].tick_params(labelsize=axis_font_size)
        ax[1].yaxis.grid()
        ax[1].set_xlabel(x_axis_label, fontsize=axis_font_size, fontweight='bold')
        ax[1].set_ylabel(y_axis_label_2, fontsize=axis_font_size, fontweight='bold')
        ax[1].set_axisbelow(True)

        ax[1].set_title('b)', loc='left')

        if ( legend_label_list_1 != legend_label_list_2 ) :
            ax[1].legend(fontsize=legend_font_size)


        # Step 6 : Save the plot

        fig.tight_layout()
        plt.savefig(filepath, bbox_inches="tight")
