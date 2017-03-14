import csv
import json
import os

path = 'data/census'

def process():
	with open('data/census.csv', 'w') as writefile:
		writer = csv.writer(writefile)
		writer.writerow(['FIPS', 'Population', 'Median Income', 'Percent White'])

		for filename in os.listdir('data/census'):
			with open('{0}/{1}'.format(path, filename)) as f:
				data = json.load(f)
				for key, item in data.items():
					row = create_row(key, item)
					writer.writerow(row)

def create_row(key, item):
	return [
		key,
		item['census']['population'],
		item['census']['median_income'],
		item['census']['percent_white']
	]

if __name__ == '__main__':
	process()