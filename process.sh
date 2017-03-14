#!/bin/bash

# create our data files
python clean.py
python combine_census.py
python election.py

# join
csvjoin -c FIPS,"County FIPS",fips data/census.csv data/county.csv data/elex.csv > data/combined.csv

