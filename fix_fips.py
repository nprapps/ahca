import csv

with open('data/combined.csv') as f, open('data/fixed_fips.csv', 'w') as g:
    reader = csv.reader(f)
    writer = csv.writer(g)

    first_row = next(reader)
    writer.writerow(first_row)

    for row in reader:
        if len(row[0]) < 5:
            row[0] = row[0].zfill(5)

        writer.writerow(row)
