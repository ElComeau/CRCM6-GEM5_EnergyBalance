#!/bin/bash

#
# This script counts the number of entries found in each station from the AmeriFlux network.
#
# Author : Élise Comeau
#
# Created : 26th of May 2021
#



# Step 1 : Define constants

DIRECTORY_PATH="/snow/comeau/AmeriFlux"
EXTENSION=".csv"


STATION_NBR_FILTER="head -n 1"               # the station number is the first match (see grep expression in Step 3)

COUNTRY_FILTER_1="head -n 2"                 # the country is the second match
COUNTRY_FILTER_2="tail -n 1"                 # (ie, the last of the two first matches)

STATION_NAME_FILTER_1="head -n 2"            # the station name is the second match
STATION_NAME_FILTER_2="tail -n 1"

FIRST_YEAR_FILTER="head -n 1"                # the first year is the first match

LAST_YEAR_FILTER="tail -n 1"                 # the last year is the last match                 


TABULATION_FILE_NAME="EntryTabulation.txt"
TABULATION_FILE_PATH="${DIRECTORY_PATH}/${TABULATION_FILE_NAME}"



# Step 2 : Obtain file list

fileNames=$(ls $DIRECTORY_PATH | grep $EXTENSION)

totalEntries=0                                   # number of entries found, all stations combined
totalStations=0                                  # number of stations (ie files) found 

for fileName in $fileNames; do

    # Step 3 : Extract the metadata

    stationNbr=$(echo $fileName | grep -oE [[:digit:]]{3} | $STATION_NBR_FILTER)                                     # the station number is made of of three (3) consecutive digits

    country=$(echo $fileName | grep -oE [[:alpha:]]{2} | $COUNTRY_FILTER_1 | $COUNTRY_FILTER_2)                      # the country is made of of two (2) consecutive alphabetic characters

    stationName=$(echo $fileName | grep -oE [[:alpha:]]{3} | $STATION_NAME_FILTER_1 | $STATION_NAME_FILTER_2)        # the station name is made up of three (3) consecutive alphabetic characters

    firstYear=$(echo $fileName | grep -oE [[:digit:]]{4} | $FIRST_YEAR_FILTER)                                       # the first year is made up of four (4) consecutive digits
    lastYear=$(echo $fileName | grep -oE [[:digit:]]{4} | $LAST_YEAR_FILTER)                                         # the last year is made up of four (4) consecutive digits



    # Step 4 : Count the number of entries in the file

    filePath="${DIRECTORY_PATH}/${fileName}"

    nbrOfLines=$(wc -l $filePath | cut -d ' ' -f 1)
    nbrOfEntries=$(( $nbrOfLines - 1 ))



    # Step 5 : Tabulate the number of stations and entries

    totalStations=$(( $totalStations + 1 ))
    totalEntries=$(( $totalEntries + $nbrOfEntries ))



    # Step 6 : Append metadata and number of entries to a tabulation file

    tabulationLine="Station_Number:${stationNbr} Station_Name:${stationName} Country:${country} First_Year:${firstYear} Last_Year:${lastYear} Number_Of_Entries:${nbrOfEntries}"

    if [[ "$totalStations" -eq 1 ]]; then                   # If this is the first tabulation ...
        echo $tabulationLine > $TABULATION_FILE_PATH       # ... then crush the previous file (if it existed).

    else                                                   # Otherwise ... 
        echo $tabulationLine >> $TABULATION_FILE_PATH      # ... append the tabulation to the already existing file.
    fi

done



# Step 7 : Append total number of stations and entries to the tabulation file

totalStationsLine="Total_Number_Of_Stations:${totalStations}"
totalEntriesLine="Total_Number_Of_Entries:${totalEntries}"

echo $totalStationsLine >> $TABULATION_FILE_PATH
echo $totalEntriesLine >> $TABULATION_FILE_PATH



# Step 8 : Show the tabulation file on terminal

cat $TABULATION_FILE_PATH
echo "PATH TO TABULATION FILE : " $TABULATION_FILE_PATH
