from openpyxl import Workbook,load_workbook
from openpyxl.utils import get_column_letter
import pandas as pd

wb = load_workbook("Draft.xlsx")
ws = wb.active
ws3 = wb["Raport Spedytor - przyklad"]
print(ws3)



for col in range(1,41):
        for row in range(ws3.min_row,ws3.max_row):
         char = get_column_letter(col)

         if ws3[char + str(row)].value == "Klient":
            print(ws3[char + str(row)].value)


#wb.save("Draft.xlsx")



