import openpyxl as xl
import pandas as pd

# Read file into panda dataframe:
workbook = xl.load_workbook('municipalities.xlsx')
# Select the sheet you want to read
sheet = workbook['נתונים פיזיים ונתוני אוכלוסייה ']

# getting data from the worksheet
city_list = []
city_symbol = []
city_status = []
city_type = []
total_pop = []
young_pop = []
for i in range(6, 261):
    # city name
    cell1 = sheet[f'A{i}']
    city = cell1.value
    city_list.append(city)
    # city symbol
    cell2 = sheet[f'B{i}']
    symbol = (cell2.value)
    city_symbol.append(symbol)
    # city status
    cell3 = sheet[f'D{i}']
    status = cell3.value
    if status == 'מועצה אזורית':
        status = 2
    else:
        status = 1
    city_status.append(status)
    # type of city (Jewish, Mixed, Arab)
    cell4 = sheet[f'P{i}']
    ctype = cell4.value
    if ctype == '-':
        ctype = 1
    elif int(ctype) > 80:
        ctype = 3
    elif 20 < int(ctype) < 80:
        ctype = 2
    else:
        ctype = 1
    city_type.append(ctype)
    # total population
    cell5 = sheet[f'M{i}']
    pop = cell5.value
    total_pop.append(pop)
    # population aged 15-29 (in %)
    cell6 = sheet[f'Y{i}']
    cell7 = sheet[f'Z{i}']
    young = cell6.value + cell7.value
    young_pop.append(young)
# dataframe consisting of six columns:
# cities, city code and city status, city type, population and youth (15-29)
df_symbol = pd.DataFrame({'Settlement_Council': city_list, 'city_code': city_symbol,
                          'city_status': city_status, 'city_type': city_type,
                          'population': total_pop, 'youth': young_pop})

# Adding 'מועצה אזורית' to the relevant municipalities
df_symbol.loc[df_symbol['city_status'] == 2, 'Settlement_Council'] = 'מועצה אזורית' + ' ' + df_symbol['Settlement_Council']
