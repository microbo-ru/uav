import pandas as pd
import re
from flightplan import parse_atc_plan, extract_subfields

# excel_file_path = '2025.xlsx'
# df = pd.read_excel(excel_file_path)
# extracted_columns = df.apply(lambda x: extract_subfields(x), axis=1, result_type="expand")
# extracted_columns.head(1000).to_csv('2025_parsed.csv', index=False, encoding='utf-8-sig')


xls = pd.ExcelFile('2024.xlsx')
all_data = []
for sheet_name in xls.sheet_names:
    if sheet_name == 'Санкт-Петербург':
        df = pd.read_excel(xls, sheet_name)
        print(df.head())
        df.to_csv('2024_spb.csv', index=False, encoding='utf-8-sig')

