def find_utc_offsets (file_pathname, nbr_of_header_rows, delimiter, station_index, utc_offset_index):

    """

    Makes a dictionary that provides UTC offsets for various stations. The keys are the station ids (country names and station name) and the values are the UTC offsets associated with the station.    


    Parameters :

        file_pathname (string)   : Absolute pathname of the file containing the UTC offsets for various stations.

        nbr_of_header_rows (int) : Number of header rows in file_pathname.

        delimiter (string)       : Delimiter used in file_pathname to seperate the variables on a line.

        station_index (int)      : Index of the station ids in file_pathname.

        utc_offset_index (int)   : Index of the UTC offsets in file_pathname.


    Returns :

        utc_offsets (dict) : Dictionary whose keys correspond to the station ids and whose values are the UTC offsets.


    Author   : Élise Comeau

    Created  : June 30th, 2021

    Modified : July 1st, 2021 


    """


    # Step 1 : Initialize variables

    utc_offsets         = {}
    utc_offset_line_nbr = 0   # line number in the utc offset file


    # Step 2 : Pair up station ids and UTC offsets

    with open(file_pathname) as utc_offset_file :

        for utc_offset_line in utc_offset_file :

            utc_offset_line_nbr = utc_offset_line_nbr + 1

            if ( utc_offset_line_nbr > nbr_of_header_rows ) :  # if we are passed the header

                country_station_name = utc_offset_line.split(delimiter)[station_index]
                utc_offset           = int(utc_offset_line.split(delimiter)[utc_offset_index])

                if ( utc_offset > 0 ) :  # since all the stations are in the Americas, all utc offsets should be negative
                    utc_offset = -1 * utc_offset

                utc_offsets.update( { country_station_name : utc_offset } )


    # Step 3 : Return dictionary

    return utc_offsets
