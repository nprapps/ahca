#!/bin/bash

# create our data files
python clean_ahca.py
python combine_census.py
python election.py
in2csv --no-inference -f xls data/original/ruralurbancodes2013.xls | csvcut -c FIPS,RUCC_2013 | csvformat -U 2 > data/codes.csv

# join
csvjoin --left -c FIPS data/ahca.csv data/census.csv data/codes.csv data/elex.csv > data/combined.csv

python fix_fips.py

# force fips codes to 

# process
python analyze.py
