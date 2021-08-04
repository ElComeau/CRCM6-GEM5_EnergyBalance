import numpy as np


def Calculate_stats(stats_names, data) :

    """

    Calculates descriptive statistics for data of one or more variables.

    
    Parameters :
    
        stats_names (list) : Names of the descriptive statistics that will be calculated (eg. mean).
    
        data (array)       : Data with which the descriptive statistics will be calculated. Each column represents a single variable.
        

    Returns :
    
        stats_values (array) : Value of the descriptive statistics.


    Author        : Élise Comeau

    Created       : June 3rd, 2021

    Last modified : August 2nd, 2021


    """


    # Step 1 : Calculate the descriptive statistics of the variable(s)

    stats_values_list = []

    for stat_name in stats_names :

        if ( stat_name == 'MEAN' ) :

            stats_values_list.append(np.mean(data, axis=0))

        elif ( stat_name == 'STANDARD_DEVIATION' ) :

            stats_values_list.append(np.std(data, axis=0))

        elif ( stat_name == 'MEDIAN' ) :

            stats_values_list.append(np.median(data, axis=0))


    # Step 2 : Return the values of the descriptive statistic(s) 

    stats_values = np.array(stats_values_list)
    return stats_values


# End of function definition
