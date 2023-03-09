# converting a dataframe to a worksheet
# using openpyxl
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
wb = Workbook()
ws = wb.active
df = 'your dataframe'

for r in dataframe_to_rows(df, index=True, header=True):
    ws.append(r)

# using pandas
import pandas as pd
df = pd.DataFrame('your data')
# to write to one sheet
df.to_excel('excel_file_path')
df.to_excel('excel_file_path', sheet_name='Sheet_name')

# to write several sheets, create an ExcelWriter object
df2 = df.copy()
with pd.ExcelWriter('excel_file_path') as writer:  
    df.to_excel(writer, sheet_name='Sheet_name_1')
    df2.to_excel(writer, sheet_name='Sheet_name_2')

# to append
with pd.ExcelWriter('excel_file_path', mode='a') as writer:  
    df.to_excel(writer, sheet_name='Sheet_name_3')


# converting a worksheet to a dataframe
import pandas as pd
wb = 'your workbook'
ws = 'your worksheet from the wb'
df = pd.DataFrame(ws.values)

# or you can use pd.read_excel()