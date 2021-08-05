import numpy as np
import glob
import os
from datetime import datetime
from datetime import timedelta
import fluxnet_classes as fc 
import pdb



"""

This script extracts the GEM dates matching those of the corresponding AmeriFlux station. The extracted GEM dates are then saved in a file.


Author        : Élise Comeau

Created       : June 23rd 2021

Last modified : June 30th 2021


"""



# Step 1 : Define constants

UTC_OFFSET_PATHNAME           = '/snow/diluca/FLUXNET_America/1990-2021/G-LE-H-LW_OUT-LW_IN-SW_OUT-SW_IN-TA-/sampling-percentage50/num-years1/Stations_GEM_1990-2021_G-LE-H-LW_OUT-LW_IN-SW_OUT-SW_IN-TA-.txt'
UTC_OFFSET_NBR_OF_HEADER_ROWS = 1  # number of header rows in the utc offset file

DELIMITER_1 = ','  # delimiter used in the utc offset and GEM files
DELIMITER_2 = '_'  # delimiter used in the AmeriFlux filenames

UTC_OFFSET_COUNTRY_STATION_INDEX = 0  # country / station name's position in the utc offset file
UTC_OFFSET_OFFSET_INDEX          = 3  # utc offset position in the utc offset file

AMF_PATHNAME    = '/snow/diluca/FLUXNET_America/1990-2021/G-LE-H-LW_OUT-LW_IN-SW_OUT-SW_IN-TA-/sampling-percentage50/num-years1/npy/*dates*'  # directory for AmeriFlux dates files; includes glob pattern to exclude other irrelevant files in the same directory (eg. data files)
GEM_DIRECTORY_R = '/snow/diluca/FLUXNET_America/GEM_1990-2017'                                                                                # the directory in which the GEM data and dates are located
GEM_DIRECTORY_W = '/snow/comeau/FLUXNET_America/GEM_1990-2017'                                                                                # directory in which the matched GEM dates will be written to

TXT_SUFFIX = '.txt'  # used to read the GEM files

AMF_COUNTRY_STATION_INDEX = 3  # country / station name's position in the AmeriFlux filenames

GEM_NBR_OF_HEADER_ROWS = 2           # number of header rows in GEM files
GEM_DATE_STR_LEN       = 10          # length of the string representing the date in the original GEM files
GEM_DATE_INDEX         = 0           # date position in the original GEM files
DATE_FORMAT            = '%Y%m%d%H'  # format of the GEM dates in their original files

AMF_T_FREQ = 3  # temporal frequency of the AmeriFlux data (ie, data are taken every 3 hours)

AMF_PREFIX = 'AMF'  # prefix of the AmeriFlux files
GEM_PREFIX = 'GEM'  # prefix of  dates files, those whose dates match those of the GEM files


# Step 2 : Obtain UTC-offsets associated with each station

utc_offsets         = {}  # utc offsets will be kept saved as dictonnaries; the keys are strings with the country and station name (eg. CA-DBB) and the values are the offsets (eg. -8)
utc_offset_line_nbr = 0   # line number in the utc offset file

with open(UTC_OFFSET_PATHNAME) as utc_offset_file :

    for utc_offset_line in utc_offset_file :

        utc_offset_line_nbr = utc_offset_line_nbr + 1

        if ( utc_offset_line_nbr > UTC_OFFSET_NBR_OF_HEADER_ROWS ) :  # if we are pasesed the header

            country_station_name = utc_offset_line.split(DELIMITER_1)[UTC_OFFSET_COUNTRY_STATION_INDEX]
            utc_offset           = int(utc_offset_line.split(DELIMITER_1)[UTC_OFFSET_OFFSET_INDEX])

            if ( utc_offset > 0 ) :  # since all the stations are in the Americas, all utc offsets should be negative
                utc_offset = -1 * utc_offset

            utc_offsets.update( { country_station_name : utc_offset } )
            #pdb.set_trace()

#pdb.set_trace()


# Step 3 : Obtain dates of an AmeriFlux station

amf_dates_pathnames = glob.glob(AMF_PATHNAME)

for amf_dates_pathname in amf_dates_pathnames :

    amf_dates = np.load(amf_dates_pathname) 
    #pdb.set_trace()


    # Step 4 : Find the corresponding GEM file and its utc offset

    amf_dates_filename   = os.path.basename(amf_dates_pathname)
    country_station_name = amf_dates_filename.split(DELIMITER_2)[AMF_COUNTRY_STATION_INDEX]

    utc_offset            = utc_offsets[country_station_name]
    utc_offset_time_delta = timedelta(hours=utc_offset)

    gem_filename_r = country_station_name + TXT_SUFFIX  # 'r' for reading
    gem_pathname_r = GEM_DIRECTORY_R + '/' + gem_filename_r   
    #pdb.set_trace()


    # Step 5 : Extract the date of the GEM file

    gem_dates = []

    gem_line_nbr = 0  # line of the GEM file currently being read

    with open(gem_pathname_r) as gem_file :

        for gem_file_line in gem_file :

            gem_line_nbr = gem_line_nbr + 1

            if ( gem_line_nbr > GEM_NBR_OF_HEADER_ROWS ) :  # if we have passed the header rows 

                gem_date_string = gem_file_line.split(DELIMITER_1)[GEM_DATE_INDEX]

                gem_date_datetime_utc   = datetime.strptime(gem_date_string, DATE_FORMAT)
                gem_date_datetime_local = gem_date_datetime_utc + utc_offset_time_delta    # conversion to local time since AmeriFlux dates are in local time

                gem_hour_local_int = gem_date_datetime_local.hour
                #pdb.set_trace()

                if ( ( gem_hour_local_int % AMF_T_FREQ ) == 0 ) : 


                    # Step 6 : Convert GEM date to AmeriFlux format

                    elapsed_time       = gem_date_datetime_local - fc.constants.reference_date
                    gem_date_formatted = elapsed_time.total_seconds()

                    gem_date_center = gem_date_formatted - ( AMF_T_FREQ / 2 ) * 3600  # to make the comparison with the AmeriFlux dates, we must take the central time of the GEM time interval
                    #pdb.set_trace()


                    # Step 7 : Verify if formatted gem date matches any of the AmeriFlux dates

                    if ( gem_date_center in amf_dates ) :
                        gem_dates.append(gem_date_center)

                    #pdb.set_trace()

                #pdb.set_trace()

            #print('Line number : ' + str(gem_line_nbr))
            #pdb.set_trace()


    # Step 8 : Write the extracted GEM dates to a file

    gem_dates_array = np.array(gem_dates)

    gem_dates_filename = amf_dates_filename.replace(AMF_PREFIX, GEM_PREFIX)
    gem_dates_pathname = GEM_DIRECTORY_W + '/' + gem_dates_filename

    np.save(gem_dates_pathname, gem_dates_array)
    #pdb.set_trace()
