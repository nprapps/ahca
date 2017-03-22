# What This Is

This script processes data from a Kaiser Family Foundation analysis of AHCA health insurance subsidies, 2016 county-level election results, USDA Rural-Uruban Continuum Codes and county-level Census data.

----------

# How To Use This

To run the analysis, first setup the repo.

```
mkvirtualenv -p `which python3` ahca
pip install -r requirements.txt
```

Then, use the process script to do everything:

```
bash process.sh
```

Your output files will be in `data/output`.

----------

# Methodology

[Kaiser Family Foundation](http://kff.org/interactive/tax-credits-under-the-affordable-care-act-vs-replacement-proposal-interactive-map/) estimated differences in federal subsidies under the proposed Republican plan in 2020 at the county level. A caveat: Kaiser's analysis at the $20,000 income level excludes Alaska, Minnesota, New York and Washington, D.C. In 2020, those residents would be eligible for Medicaid (Alaska and Washington, D.C.) or the Basic Health Program (Minnesota and New York).

We grouped each county into one of three groups based on its [USDA Rural-Urban Continuum Code](https://www.ers.usda.gov/data-products/rural-urban-continuum-codes/). Metro counties had a code between 1 and 3, small town counties had a code between 4 and 7, rural counties had a code of either 8 or 9.

Election results data came from the Associated Press. These results were last updated on November 28, 2016, and are not the final certified results. The average vote calculations for rural, smaller and metro counties do not include Alaska, as the AP does not report election results on the county level in Alaska.

We calculated an average value for each county grouping, weighted by population. For each county, we multiplied the county's dollar difference for each age and income bracket by the county's population (according to 2015 American Community Survey 5-Year data) to create a weighted score. Then, for each county grouping (metro, small town, metro), we summed the weighted scores for each age and income bracket and divided it by the summed population of those county groupings.
