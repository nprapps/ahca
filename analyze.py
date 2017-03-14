import agate
import leather

number_type = agate.Number()

def calculate_percent_enrolled(row):
	return row['Plan Selections'] / row['Population']

signups = agate.Table.from_csv('data/combined.csv')
percent_enrolled = signups.compute([
	('percent_enrolled', agate.Formula(number_type, calculate_percent_enrolled))
])

trump = percent_enrolled.where(lambda r: r['trump_votepct'] > r['clinton_votepct'])
clinton = percent_enrolled.where(lambda r: r['clinton_votepct'] > r['trump_votepct'])

print(trump.aggregate(agate.Mean('percent_enrolled')))
print(clinton.aggregate(agate.Mean('percent_enrolled')))

outlier = percent_enrolled.order_by('percent_enrolled', reverse=True).rows[0]

print(outlier['County Name'], outlier['State'], outlier['percent_enrolled'], outlier['Population'], outlier['Plan Selections'])

percent_enrolled.scatterplot('trump_votepct', 'percent_enrolled', 'trump_vs_enrollment.svg')
percent_enrolled.scatterplot('Median Income', 'percent_enrolled', 'income_vs_enrollment.svg')
percent_enrolled.scatterplot('Percent White', 'percent_enrolled', 'white_vs_enrollment.svg')
