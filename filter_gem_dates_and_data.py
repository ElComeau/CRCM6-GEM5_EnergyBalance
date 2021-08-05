import numpy as np
from datetime import datetime
from datetime import timedelta
import fluxnet_classes as fc 
import pdb



"""

This script extracts the GEM dates matching those of the corresponding AmeriFlux station.
VERSION 1 : Script works with only 1 GEM station and 1 AmeriFlux station.


Author        : Élise Comeau

Created       : June 23rd 2021

Last modified : June 29th 2021


"""



# Step 1 : Define constants

GEM_DIRECTORY_R     = '/snow/diluca/FLUXNET_America/GEM_1990-2018'                                                                        # the directory in which the GEM data and dates are located
AMERIFLUX_DIRECTORY = '/snow/diluca/FLUXNET_America/1990-2021/G-LE-H-LW_OUT-LW_IN-SW_OUT-SW_IN-TA-/sampling-percentage50/num-years1/npy'  # directory for AmeriFlux data and dates
GEM_DIRECTORY_W     = '/snow/comeau/FLUXNET_America/GEM'                                                                                  # directory in which the matched GEM dates will be written to

NBR_OF_HEADER_ROWS = 2    # number of header rows in GEM files
DELIMITER          = ','  # delimiter used in the GEM files

DATE_FORMAT = '%Y%m%d%H'  # format of the GEM dates

AMF_PREFIX = 'AMF'  # prefix of the AmeriFlux files
GEM_PREFIX = 'GEM'  # prefix of  dates files, those whose dates match those of the GEM files


# Step 2 : Obtain dates of the AmeriFlux station

ameriflux_dates_filename = 'AMF_dates_042_US-Wrc_1990-2021_G-LE-H-LW_OUT-LW_IN-SW_OUT-SW_IN-TA-_3.npy'
ameriflux_dates_pathname = AMERIFLUX_DIRECTORY + '/' + ameriflux_dates_filename

ameriflux_dates = np.load(ameriflux_dates_pathname)

pdb.set_trace()


# Step 3 : Read the GEM file

gem_filename_r = 'US-Wrc.txt'
gem_pathname_r = GEM_DIRECTORY_R + '/' + gem_filename_r

with open(gem_pathname_r) as gem_file :
    gem_file_content = gem_file.readlines()[NBR_OF_HEADER_ROWS:]

#pdb.set_trace()


# Step 4 : Extract date of the GEM file

gem_dates = []

for gem_file_line in gem_file_content :

    gem_date_string = gem_file_line.split(DELIMITER)[0]


    # Step 5 : Convert GEM date to AmeriFlux format

    gem_date_datetime  = datetime.strptime(gem_date_string, DATE_FORMAT)
    elapsed_time       = gem_date_datetime - fc.constants.reference_date
    gem_date_formatted = elapsed_time.total_seconds()


    # Step 6 : Verify if formatted gem date matches any of the AmeriFlux dates

    if ( gem_date_formatted in ameriflux_dates ) :
        gem_dates.append(gem_date_formatted)

#    pdb.set_trace()

#pdb.set_trace()


# Step 7 : Write the extracted GEM dates to a file

gem_dates_array = np.array(gem_dates)

gem_dates_filename = ameriflux_dates_filename.replace(AMF_PREFIX, GEM_PREFIX)
gem_dates_pathname = GEM_DIRECTORY_W + '/' + gem_dates_filename

np.save(gem_dates_pathname, gem_dates_array)

#pdb.set_trace()
