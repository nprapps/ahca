import agate

text_type = agate.Text()
number_type = agate.Number()
specified_types = {
    'FIPS': text_type
}

ahca = agate.Table.from_csv('data/fixed_fips.csv', column_types=specified_types)

trump = ahca.where(lambda r: r['trump_votecount'] > r['clinton_votecount'])
clinton = ahca.where(lambda r: r['clinton_votecount'] > r['trump_votecount'])
rural = ahca.where(lambda r: r['RUCC_2013'] > 7)
small_towns = ahca.where(lambda r: 3 < r['RUCC_2013'] <= 7)
metro = ahca.where(lambda r: r['RUCC_2013'] <= 3)

ages = ['27', '40', '60']
incomes = ['20', '30', '40', '50', '75']

def print_breakdown():
    for age in ages:
        for income in incomes:
            print(
                '{0} with {1} \n'.format(age, income),
                'Trump:',
                trump.aggregate(agate.Mean('Dollar difference for {0} year old with ${1},000 income'.format(age, income))),
                '\n',
                'Clinton:',
                clinton.aggregate(agate.Mean('Dollar difference for {0} year old with ${1},000 income'.format(age, income))),
                '\n',
                'Rural:',
                rural.aggregate(agate.Mean('Dollar difference for {0} year old with ${1},000 income'.format(age, income))),
                '\n',
                'Small Towns:',
                small_towns.aggregate(agate.Mean('Dollar difference for {0} year old with ${1},000 income'.format(age, income))),
                '\n',
                'Metro:',
                metro.aggregate(agate.Mean('Dollar difference for {0} year old with ${1},000 income'.format(age, income)))
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
        'trump_votepct',
        'clinton_votepct'
    ]

    ahca.select(include).to_csv('data/output/all.csv')
    trump.select(include).to_csv('data/output/trump_counties.csv')
    clinton.select(include).to_csv('data/output/clinton_counties.csv')
    rural.select(include).to_csv('data/output/rural_counties.csv')
    small_towns.select(include).to_csv('data/output/town_counties.csv')
    metro.select(include).to_csv('data/output/metro_counties.csv')


class WeightedScore(agate.Computation):
    def __init__(self, column_name):
        self.column_name = column_name

    def get_computed_data_type(self, table):
        return number_type

    def run(self, table):
        new_column = []

        for row in table.rows:
            if row[self.column_name] is not None:
                weighted_score = row[self.column_name] * row['Population']
                new_column.append(weighted_score)
            else:
                new_column.append(None)

        return new_column



def write_weighted_means_csv():
    counties = [(rural_weighted, 'rural'), (small_towns_weighted, 'small_towns'), (metro_weighted, 'metro')]

    column_names = ['county_type']
    column_types = [text_type]
    for age in ages:
        for income in incomes:
            column_names.append('weighted_mean_{0}yo_{1}k'.format(age, income))
            column_types.append(number_type)

    rows = []
    for county in counties:
        row = [county[1]]
        total_population = county[0].aggregate(agate.Sum('Population'))
        for age in ages:
            for income in incomes:
                score = county[0].aggregate(agate.Sum('weighted_score_{0}yo_{1}k'.format(age, income)))
                row.append(score / total_population)

        rows.append(row)

    table = agate.Table(rows, column_names, column_types).to_csv('data/output/weighted_means.csv')   

if __name__ == '__main__':
    # print_breakdown()
    # write_csvs()

    rural_weighted = rural.compute([
        ('weighted_score_27yo_20k', WeightedScore('Dollar difference for 27 year old with $20,000 income')),
        ('weighted_score_27yo_30k', WeightedScore('Dollar difference for 27 year old with $30,000 income')),
        ('weighted_score_27yo_40k', WeightedScore('Dollar difference for 27 year old with $40,000 income')),
        ('weighted_score_27yo_50k', WeightedScore('Dollar difference for 27 year old with $50,000 income')),
        ('weighted_score_27yo_75k', WeightedScore('Dollar difference for 27 year old with $75,000 income')),
        ('weighted_score_40yo_20k', WeightedScore('Dollar difference for 40 year old with $20,000 income')),
        ('weighted_score_40yo_30k', WeightedScore('Dollar difference for 40 year old with $30,000 income')),
        ('weighted_score_40yo_40k', WeightedScore('Dollar difference for 40 year old with $40,000 income')),
        ('weighted_score_40yo_50k', WeightedScore('Dollar difference for 40 year old with $50,000 income')),
        ('weighted_score_40yo_75k', WeightedScore('Dollar difference for 40 year old with $75,000 income')),
        ('weighted_score_60yo_20k', WeightedScore('Dollar difference for 60 year old with $20,000 income')),
        ('weighted_score_60yo_30k', WeightedScore('Dollar difference for 60 year old with $30,000 income')),
        ('weighted_score_60yo_40k', WeightedScore('Dollar difference for 60 year old with $40,000 income')),
        ('weighted_score_60yo_50k', WeightedScore('Dollar difference for 60 year old with $50,000 income')),
        ('weighted_score_60yo_75k', WeightedScore('Dollar difference for 60 year old with $75,000 income')),
    ])

    small_towns_weighted = small_towns.compute([
        ('weighted_score_27yo_20k', WeightedScore('Dollar difference for 27 year old with $20,000 income')),
        ('weighted_score_27yo_30k', WeightedScore('Dollar difference for 27 year old with $30,000 income')),
        ('weighted_score_27yo_40k', WeightedScore('Dollar difference for 27 year old with $40,000 income')),
        ('weighted_score_27yo_50k', WeightedScore('Dollar difference for 27 year old with $50,000 income')),
        ('weighted_score_27yo_75k', WeightedScore('Dollar difference for 27 year old with $75,000 income')),
        ('weighted_score_40yo_20k', WeightedScore('Dollar difference for 40 year old with $20,000 income')),
        ('weighted_score_40yo_30k', WeightedScore('Dollar difference for 40 year old with $30,000 income')),
        ('weighted_score_40yo_40k', WeightedScore('Dollar difference for 40 year old with $40,000 income')),
        ('weighted_score_40yo_50k', WeightedScore('Dollar difference for 40 year old with $50,000 income')),
        ('weighted_score_40yo_75k', WeightedScore('Dollar difference for 40 year old with $75,000 income')),
        ('weighted_score_60yo_20k', WeightedScore('Dollar difference for 60 year old with $20,000 income')),
        ('weighted_score_60yo_30k', WeightedScore('Dollar difference for 60 year old with $30,000 income')),
        ('weighted_score_60yo_40k', WeightedScore('Dollar difference for 60 year old with $40,000 income')),
        ('weighted_score_60yo_50k', WeightedScore('Dollar difference for 60 year old with $50,000 income')),
        ('weighted_score_60yo_75k', WeightedScore('Dollar difference for 60 year old with $75,000 income')),
    ])

    metro_weighted = metro.compute([
        ('weighted_score_27yo_20k', WeightedScore('Dollar difference for 27 year old with $20,000 income')),
        ('weighted_score_27yo_30k', WeightedScore('Dollar difference for 27 year old with $30,000 income')),
        ('weighted_score_27yo_40k', WeightedScore('Dollar difference for 27 year old with $40,000 income')),
        ('weighted_score_27yo_50k', WeightedScore('Dollar difference for 27 year old with $50,000 income')),
        ('weighted_score_27yo_75k', WeightedScore('Dollar difference for 27 year old with $75,000 income')),
        ('weighted_score_40yo_20k', WeightedScore('Dollar difference for 40 year old with $20,000 income')),
        ('weighted_score_40yo_30k', WeightedScore('Dollar difference for 40 year old with $30,000 income')),
        ('weighted_score_40yo_40k', WeightedScore('Dollar difference for 40 year old with $40,000 income')),
        ('weighted_score_40yo_50k', WeightedScore('Dollar difference for 40 year old with $50,000 income')),
        ('weighted_score_40yo_75k', WeightedScore('Dollar difference for 40 year old with $75,000 income')),
        ('weighted_score_60yo_20k', WeightedScore('Dollar difference for 60 year old with $20,000 income')),
        ('weighted_score_60yo_30k', WeightedScore('Dollar difference for 60 year old with $30,000 income')),
        ('weighted_score_60yo_40k', WeightedScore('Dollar difference for 60 year old with $40,000 income')),
        ('weighted_score_60yo_50k', WeightedScore('Dollar difference for 60 year old with $50,000 income')),
        ('weighted_score_60yo_75k', WeightedScore('Dollar difference for 60 year old with $75,000 income')),
    ])

    write_weighted_means_csv()