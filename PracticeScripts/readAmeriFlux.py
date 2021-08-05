"""
 This script reads csv files containing data from AmeriFlux. It extracts the variables described in this file and removes the unecessary ones.
 It also calculates missing values for certain variables. All complete entries are written to a new file. A graph is also produced.


 Author : Elise Comeau

"""




# Step 1 : Import packages

import pandas as pd
import csv
import os
import re
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates




# Step 2 : Define constants

INDEX_FIRST_LINE = 0
INDEX_COUNTRY    = 2
INDEX_STATION    = 3

CSV_EXT          = '.csv'
DIR_NAME_R       = '/HOME/data/Validation/AmeriFlux'          # name of the directory from which the files will be read

INDEX_ROW_COUNT  = 0
ABSENT_VALUE     = -9999
INDEX_YEAR       = 4 

DIR_NAME_W       = '/snow/comeau/AmeriFlux'                   # name of the directory in which the (data) files will be written
DIR_NAME_W_G     = '/snow/comeau/AmeriFlux/png'               # name of the directory in which the png files will be written



# Step 3 : Obtain list of files to read

dirContent = os.listdir(DIR_NAME_R)

fileNames = []

for file in dirContent :
    if CSV_EXT in file:
        fileNames.append(file)




# Step 4 : Process file

stationNumber = 1   # only files that are kept are counted

for fileName in fileNames:

    # Step 4.1 : Extract country and station name

    filePath = os.path.join(DIR_NAME_R, fileName)
    print('Reading file : ' + str(filePath))

    with open(filePath) as file:
        reader = csv.reader(file)
        metaData = next(reader)[INDEX_FIRST_LINE]

    splitMetaData = re.split(' |-', metaData)

    country = splitMetaData[INDEX_COUNTRY]
    station = splitMetaData[INDEX_STATION]

    print('Country : ' + country)
    print('Station : ' + station + '\n')


    # Step 4.2 : Verify if the station is in a country that is of interest

    countries = {'CA':'Canada', 'US':'United States'}    # list of countries that are of interest to us
    countryKeys = countries.keys()
    countryPresent = False                               # is the country of the current file one that interests us?

    for aCountry in countries :

        if ( country == aCountry ) :       # if the country of the current file is one that interests us
            countryPresent = True

    if (countryPresent) : # Steps 5 and onward only apply if the country of the current file is one that interests us



        # Step 5 : Filter the data

        # Step 5.1 : Verify which variables are present in the data

        # Step 5.1.1 : Verify the presence of each variable we want individually

        data = pd.read_csv(filePath, sep=',', header=2)


        # names of the variables we want to extract; these variables must be present in the data :
        varNames = {'TIMESTAMP_START':'Start of averaging period', 'TIMESTAMP_END':'End of averaging period', 'G':'Soil Heat FLux', 'H':'Sensible Heat Turbulent Flux (no storage correction)', 
                    'LE':'Latent Heat Turbulent FLux (no storage correction)', 'LW_IN':'Longwave radiation, incoming', 'LW_OUT':'Longwave radiation, outgoing', 'SW_IN':'Shortwave radiation, incoming',
                    'SW_OUT':'Shortwave radiation, outgoing'}
 
        # are the variables we want present in the data ?
        varPresent = {'TIMESTAMP_START':'False', 'TIMESTAMP_END':'False', 'G':'False', 'H':'False', 'LE':'False', 'LW_IN':'False', 'LW_OUT':'False', 'SW_IN':'False', 'SW_OUT':'False'}

        varExtra = {'ALB':'Albedo from 0 to 100', 'NETRAD':'Net radiation'} # these variables are not required to present in the data, but we are still interested in them

        varKeys      = varNames.keys()   # note that the keys of varNames and varPresent are identical
        varExtraKeys = varExtra.keys()
        dataColumns  = data.columns      # names of the variables (ie columns) present in the data

        for varName in varKeys: # For each variable we want ...

            for dataColumn in dataColumns:         # ... compare it against each column (ie variable) from the data.

                if (varName == dataColumn):        # If you find one of the variables we want in the data ...
                    varPresent[varName] = 'True'   # ... then this variable is marked as "present".

            print(varName + ' is present in the data : ' + varPresent[varName])


        # Step 5.1.2 : Verify whether all the variables we want are present in the data

        varsAllPresent = True      # have all the variables been found in the data?

        for varName in varKeys:

         if (varPresent[varName] == 'False'):    # If at least one of the variables we want is not present ...
             varsAllPresent = False              # ... than we cannot say that all the variables we want are present.

        print('\nAll the variables are present : ' + str(varsAllPresent) + '\n')



        # Step 5.2 : Filter out data we are not interested in (if applicable)

        if(varsAllPresent): # Step 5.2 only applies to those data sets that had all the variables we are looking for

            # Step 5.2.1 : Remove variables (ie columns) that we are not interested in from the data

            for dataColumn in dataColumns:                        # For each variable (column) in the data ...

                if ( (dataColumn not in varKeys) and (dataColumn not in varExtraKeys) ):            # ... if the variable is not one in which we are intered in ...
                    data.drop(dataColumn, inplace=True, axis=1)                                     # ... remove the variable from the data.

            dataColumns = data.columns


            # Step 5.2.2 : Remove rows (ie data entries) with absent data

            for dataColumn in dataColumns:

                data = data[ data[dataColumn] != ABSENT_VALUE]

            rowCount = data.shape[INDEX_ROW_COUNT]


            # Step 5.2.3 : Verify if there is at least one year's worth of remaining data
          
            timeDif = datetime.timedelta(days = 0)
            aYear   = datetime.timedelta(days = 365) # ie, 1 year

            if (rowCount >= 2) :

                initialDateTime = pd.to_datetime( data['TIMESTAMP_START'].iloc[0], format='%Y%m%d%H%M' )
                finalDateTime   = pd.to_datetime( data['TIMESTAMP_END'].iloc[rowCount - 1], format='%Y%m%d%H%M' )
                timeDif         = finalDateTime - initialDateTime

            if ( timeDif >= aYear ) : # if there's at least a one year's worth of data ...

                # Step 5.2.4 : Add missing data (extra variables only)

                dataColumns = data.columns
 
                if ('NETRAD' in dataColumns) :                                                                                                                 # If the data already has a variable 'NETRAD' ...

                    for i in range(0, (rowCount - 1)) :

                        if ( data['NETRAD'].iloc[i] == ABSENT_VALUE ) :                                                                                        # ... verify if there are no missing values. If there are missing values ... 
                            data['NETRAD'].iloc[i] = ( data['LW_IN'].iloc[i] - data['LW_OUT'].iloc[i] ) + ( data['SW_IN'].iloc[i] - data['SW_OUT'].iloc[i] )   # ... then calculate it.

                else :                                                                                                                                         # Otherwise ...
                    data['NETRAD*'] = ( data['LW_IN'] - data['LW_OUT'] ) + ( data['SW_IN'] - data['SW_OUT'] )                                                  # ... create the variable 'NETRAD'.                                                 


                if ('ALB' in dataColumns) :                                                                  # The procedure for 'ALB' is identical to that of 'NETRAD'.

                    for i in range(0, (rowCount - 1)) :

                        if ( data['ALB'].iloc[i] == ABSENT_VALUE ) :
                            data['ALB'].iloc[i] = ( data['SW_OUT'].iloc[i] / data['SW_IN'].iloc[i] ) * 100    # only the Sun's radiation is considered for the albedo

                else :
                    data['ALB*'] = ( data['SW_OUT'] / data['SW_IN'] ) * 100      
      


            # Step 6 : Write to file (if applicable)

            if ( (varsAllPresent) and (timeDif >= aYear) ) : # Step 6 only applies if all the variables we are interested in are present in the data 

                # Step 6.1 : Write filtered data to file

                stationNumberStr = str(stationNumber).zfill(3)

                firstDateTime  = data['TIMESTAMP_START'].iloc[INDEX_FIRST_LINE]      # date and time at which first measurement was taken
                lastDateTime   = data['TIMESTAMP_START'].iloc[rowCount - 1]          # date and time at which last measurement was taken  
                firstYear      = str(firstDateTime)[:INDEX_YEAR]                     # year during which first measurement was taken
                lastYear       = str(lastDateTime)[:INDEX_YEAR]                      # year during which last measurement was taken

                fileName = 'AMF_' + stationNumberStr + '_' +  country + '-' + station + '_' + firstYear + '-' + lastYear + '.csv'
                filePath = os.path.join(DIR_NAME_W, fileName)
                data.to_csv(filePath, index=False)

                print('Writing data to file : ' + filePath + '\n\n\n')
                stationNumber += 1



                # Step 6.2 : Write png (graph) to file

                datesDt = pd.to_datetime( data['TIMESTAMP_START'].iloc[0:20], format='%Y%m%d%H%M')
                firstDate = datesDt.iloc[0]
                lastDate = datesDt.iloc[19]
                sw_in = data['SW_IN'].iloc[0:20]
  
                fig = plt.figure(figsize=(20,5))
                ax = fig.add_subplot(111)
                ax.plot(datesDt, sw_in)

                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
                plt.xlabel('Time')
                plt.ylabel('Shortwave radiation, incoming (W * m⁻2)')
                plt.title('Solar radiation received at the surface from ' + str(firstDate) + ' to ' + str(lastDate) + ' at ' + station + ' station (' + country + ')')
                plt.grid(True)

                fileNameGraph = fileName = 'AMF_' + stationNumberStr + '_' +  country + '-' + station + '_' + firstYear + '-' + lastYear + '.png'
                filePathGraph = os.path.join(DIR_NAME_W_G, fileNameGraph)
                plt.savefig(filePathGraph)  

            else :                                                       
                print('At least one variable is absent. Data will not be saved. \n\n\n')

        else :
            print('Less than one year\'s worth of data is left after removing rows with absent values. Data will not be saved. \n\n\n')

    else :
        print('The country in which the station is located is not part of the targeted countries. Data will not be read. \n\n\n')   # if the country is not of interest to us
