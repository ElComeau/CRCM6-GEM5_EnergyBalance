import numpy as np
import datetime
from datetime import timedelta



def Get_datetime_index(datetime_array, specific_datetime) :

    """
    Finds the index of the datetime closest to a specific datetime.


    Parameters :

        datetime_array (array)       : One dimensional array filled with datetimes.

        specific_datetime (datetime) : Specific datetime which must be matched as closely as possible.


    Returns :

        datetime_index (int) : Index of the datetime closest to specific_datetime.


    Author        : Élise Comeau

    Created       : August 4th 2021

    Last modified : August 4th 2021 

    """

    min_datetime_difference = abs( datetime_array[0] - specific_datetime )
    min_datetime            = datetime_array[0]    

    amount_of_datetimes = datetime_array.shape[0]

    if ( amount_of_datetimes > 1 ) :

        for datetime in datetime_array :

            datetime_difference = abs( datetime - specific_datetime )

            if ( datetime_difference < min_datetime_difference ) :

                min_datetime_difference = datetime_difference
                min_datetime            = datetime

    datetime_indexes = np.where(datetime_array == min_datetime)       
    datetime_index   = int( datetime_indexes[0][0] )

    return datetime_index
