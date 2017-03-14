import csv
import openpyxl

wb = openpyxl.load_workbook('data/original/tax-credits-in-2020-for-single-coverage-under-the-aca-vs-the-ahca.xlsx')
sheet = wb.get_sheet_by_name('2020 ACA subsidy vs House tax c')


column_letters = ['A', 'C', 'E', 'N', 'O', 'P', 'Q', 'R', 'S', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF']
county_data = sheet['A5':'BM3148']

with open('data/ahca.csv', 'w') as f:
    writer = csv.writer(f)

    for row in county_data:
        output_row = []

        for cell in row:
            if cell.column in column_letters:
                output_row.append(cell.value)

        writer.writerow(output_row)