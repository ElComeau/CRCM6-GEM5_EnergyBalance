import datetime
import pdb



def epoch_to_datetime (epoch_dates, reference_date) :

    """
    Converts epoch dates to datetime format.


    Parameters :

        epoch_dates (list)               : List of epoch dates in seconds. Epoch dates are assumed to be time differences since reference_date.

        reference_date (datetime object) : Reference date from which epoch dates were calculated.


    Returns :

        datetime_dates (list)            : Datetime dates obtained from the list of epoch dates.


    Author        : Élise Comeau

    Created	  : July 28th, 2021

    Last modified : July 28th, 2021


    """


    datetime_dates = []

    for epoch_date in epoch_dates :

        #pdb.set_trace()
        timedelta_date = datetime.timedelta(seconds=int(epoch_date))
        datetime_date  = reference_date + timedelta_date

        datetime_dates.append(datetime_date)

    return datetime_dates
