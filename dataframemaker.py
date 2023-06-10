import pandas as pd
import update


# UNCOMMENT THIS LINE TO UPDATE CRIME DATA FROM INTERNET
update.data_update()

df = pd.read_csv('output.csv', dtype={'city_code': str}, index_col=0)
df['city_code'] = df['city_code'].fillna('')

# Making dataframe with same period data (relevant if Q4 is not last data available)
# latest year represented in data
latest_year = (sorted(df['year'].unique())[-1])
# temp dataframe consisting only of latest year data
df_temp = df[df['year'] == latest_year]
# getting last quarter in the dataframe of latest year data
latest_quarter = (sorted(df_temp['quarter'])[-1])
# making the adjusted dataframe for same period across the years (df_quarter)
unique_quarters = (df_temp['quarter'].unique()).tolist()
df_quarter = df.loc[(df['quarter'].isin(unique_quarters))]
# there are now two dataframes:
#   df is the dataframe of all data
#   df_quarter is the dataframe for same period across the years
