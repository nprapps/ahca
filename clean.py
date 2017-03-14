import csv
import openpyxl

wb = openpyxl.load_workbook('data/original/mar2016marketplacezipcode_1.xlsx')
sheet = wb.get_sheet_by_name('County ')
county_data = sheet['A23':'D2622']

with open('data/county.csv', 'w') as f:
    writer = csv.writer(f)
    for row in county_data:
        writer.writerow([cell.value for cell in row])

