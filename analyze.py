import agate
import leather

specified_types = {
    'FIPS': agate.Text()
}

ahca = agate.Table.from_csv('data/fixed_fips.csv', column_types=specified_types)

trump = ahca.where(lambda r: r['trump_votecount'] > r['clinton_votecount'])
clinton = ahca.where(lambda r: r['clinton_votecount'] > r['trump_votecount'])

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
                'Trump:',
                trump.aggregate(agate.Mean('Dollar difference for {0} year old with {1} income'.format(age, income))),
                '\n',
                'Clinton:',
                clinton.aggregate(agate.Mean('Dollar difference for {0} year old with {1} income'.format(age, income))),
                '\n',
                'Rural:',
                rural.aggregate(agate.Mean('Dollar difference for {0} year old with {1} income'.format(age, income))),
                '\n',
                'Small Towns:',
                small_towns.aggregate(agate.Mean('Dollar difference for {0} year old with {1} income'.format(age, income))),
                '\n',
                'Metro:',
                metro.aggregate(agate.Mean('Dollar difference for {0} year old with {1} income'.format(age, income)))
            )

    print(
        'Trump vote percentage in rural counties:',
        calculate_trump_pct(rural),
        '\n',
        'Trump vote percentage in small town counties:',
        calculate_trump_pct(small_towns),
        '\n',
        'Trump vote percentage in metro counties:',
        calculate_trump_pct(metro),
    )

def calculate_trump_pct(table):
    trump_total = table.aggregate(agate.Sum('trump_votecount'))

    other_total = 0
    for cand in ['clinton', 'johnson', 'stein', 'mcmullin', 'other']:
        other_total += table.aggregate(agate.Sum('{0}_votecount'.format(cand)))

    return (trump_total / (trump_total + other_total)) * 100

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
        'trump_votecount',
        'clinton_votecount'
    ]

    ahca.select(include).to_csv('data/output/all.csv')
    trump.select(include).to_csv('data/output/trump_counties.csv')
    clinton.select(include).to_csv('data/output/clinton_counties.csv')
    rural.select(include).to_csv('data/output/rural_counties.csv')
    small_towns.select(include).to_csv('data/output/town_counties.csv')
    metro.select(include).to_csv('data/output/metro_counties.csv')


    ages = ['27', '40', '60']
    incomes = ['$20,000', '$30,000', '$40,000', '$50,000', '$75,000']
    counties = [(rural, 'rural'), (small_towns, 'small_towns'), (metro, 'metro')]

    column_names = ['county_type']
    for age in ages:
        for income in incomes:
            column_names.append('dollar_diff_{0}yo_{1}k'.format(age, income[1:3]))
    
    column_types = [agate.Text()]
    for i in range(15):
        column_types.append(agate.Number())

    rows = []
    for county in counties:
        row = [county[1]]
        
        for age in ages:
            for income in incomes:
                row.append(county[0].aggregate(agate.Mean('Dollar difference for {0} year old with {1} income'.format(age, income))))

        rows.append(row)

    table = agate.Table(rows, column_names, column_types).to_csv('data/output/means.csv')



if __name__ == '__main__':
    print_breakdown()
    write_csvs()

    # calculate_trump_pct(rural)

    # ahca.select([
    #     'ST',
    #     'County',
    #     "Dollar difference for 60 year old with $20,000 income",
    #     'Population'
    # ]).where(lambda r: r['ST'] == 'TX').order_by('Population', reverse=True).print_table(10)