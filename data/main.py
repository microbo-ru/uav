import pandas as pd
import re
from flightplan import parse_atc_plan, extract_subfields

excel_file_path = '2025.xlsx'
df = pd.read_excel(excel_file_path)

extracted_columns = df.apply(lambda x: extract_subfields(x), axis=1, result_type="expand")

extracted_columns.head(1000).to_csv('2025_parsed.csv', index=False, encoding='utf-8-sig')

