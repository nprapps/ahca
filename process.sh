#!/bin/bash

# create our data files
python clean.py
python combine_census.py
python election.py

# join
csvjoin -c FIPS,FIPS,fips data/ahca.csv data/census.csv data/elex.csv > data/combined.csv

# process
