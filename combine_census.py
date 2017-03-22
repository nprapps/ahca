import csv
import json
import os
import requests

path = 'data/census'
CENSUS_REPORTER_URL = 'http://api.censusreporter.org/1.0/data/show/latest'
FIPS_TEMPLATE = '05000US{0}'
TABLES = ['B01003']

def process():
    with open('data/census.csv', 'w') as writefile:
        writer = csv.writer(writefile, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(['FIPS', 'Population'])

        with open('data/ahca.csv', 'r') as readfile:
            reader = csv.reader(readfile)
            next(reader)
            for row in reader:
                fips = row[0]
                
                if fips == '46113':
                    real_fips = '46102'
                    geo_id = FIPS_TEMPLATE.format(real_fips)
                elif fips == '02270':
                    real_fips = '02158'
                    geo_id = FIPS_TEMPLATE.format(real_fips)
                else:
                    geo_id = FIPS_TEMPLATE.format(fips)

                params = {
                    'geo_ids': geo_id,
                    'table_ids': ','.join(TABLES)
                }

                r = requests.get(CENSUS_REPORTER_URL, params=params)
                if r.status_code != 200:
                    print(fips, r.status_code, r.url)
                else:
                    print(fips)
                    response = r.json()
                    data = response.get('data').get(geo_id)
                    population = data['B01003']['estimate']['B01003001']
                    writer.writerow([fips, population])


def create_row(key, item):
    return [
        key,
        item['census']['population'],
    ]

if __name__ == '__main__':
    process()