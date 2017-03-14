import agate
import leather

ahca = agate.Table.from_csv('data/combined.csv')

trump = ahca.where(lambda r: r['trump_votepct'] > r['clinton_votepct'])
clinton = ahca.where(lambda r: r['clinton_votepct'] > r['trump_votepct'])

rural = ahca.where(lambda r: r['RUCC_2013'] > 7)
small_towns = ahca.where(lambda r: 3 < r['RUCC_2013'] <= 7)
metro = ahca.where(lambda r: r['RUCC_2013'] <= 3)

def print_breakdown():
    ages = ['27', '40', '60']
    incomes = ['$20,000', '$30,000', '$40,000', '$50,000', '$75,000']

    for age in ages:
        for income in incomes:
            print(
                '{0} with {1} \n'.format(age, income),
                'Trump: ',
                trump.aggregate(agate.Mean('Dollar difference for {0} year old with {1} income'.format(age, income))),
                '\n',
                'Clinton: ',
                clinton.aggregate(agate.Mean('Dollar difference for {0} year old with {1} income'.format(age, income))),
                '\n',
                'Rural: ',
                rural.aggregate(agate.Mean('Dollar difference for {0} year old with {1} income'.format(age, income))),
                '\n',
                'Small Towns: ',
                small_towns.aggregate(agate.Mean('Dollar difference for {0} year old with {1} income'.format(age, income))),
                '\n',
                'Metro: ',
                metro.aggregate(agate.Mean('Dollar difference for {0} year old with {1} income'.format(age, income)))
            )

def write_csvs():
    include = [
        'FIPS',
        'ST',
        'County',
        "Dollar difference for 27 year old with $20,000 income",
        "Dollar difference for 27 year old with $30,000 income",
        "Dollar difference for 27 year old with $40,000 income",
        "Dollar difference for 27 year old with $50,000 income",
        "Dollar difference for 40 year old with $20,000 income",
        "Dollar difference for 40 year old with $30,000 income",
        "Dollar difference for 40 year old with $40,000 income",
        "Dollar difference for 40 year old with $50,000 income",
        "Dollar difference for 60 year old with $20,000 income",
        "Dollar difference for 60 year old with $30,000 income",
        "Dollar difference for 60 year old with $40,000 income",
        "Dollar difference for 60 year old with $50,000 income",
        'RUCC_2013',
        'trump_votepct',
        'clinton_votepct'
    ]

    ahca.select(include).to_csv('data/output/all.csv')
    trump.select(include).to_csv('data/output/trump_counties.csv')
    clinton.select(include).to_csv('data/output/clinton_counties.csv')
    rural.select(include).to_csv('data/output/rural_counties.csv')
    small_towns.select(include).to_csv('data/output/town_counties.csv')
    metro.select(include).to_csv('data/output/metro_counties.csv')

if __name__ == '__main__':
    print_breakdown()
    write_csvs()