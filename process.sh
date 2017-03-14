#!/bin/bash

# create our data files
python clean.py
python combine_census.py
python election.py
in2csv -f xls data/original/ruralurbancodes2013.xls | csvcut -c FIPS,RUCC_2013 > data/codes.csv

# join
csvjoin -c FIPS,FIPS,FIPS,fips data/ahca.csv data/census.csv data/codes.csv data/elex.csv > data/combined.csv

# process
python analyze.py