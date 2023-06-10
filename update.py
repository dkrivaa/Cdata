import requests
import pandas as pd
import json
from municipalities import df_symbol


def data_update():
    # FIRST PART OF UPDATE
    # getting the count of records
    url = "https://data.gov.il/api/3/action/datastore_search?resource_id=5fc13c50-b6f3-4712-b831-a75e0f91a17e"

    # Make a GET request to the API endpoint
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response JSON
        data = json.loads(response.text)

        # Extract the count of records
        count = data["result"]["total"]

    # SECOND PART OF UPDATE
    # doing the actual update of the data file
    url = 'https://data.gov.il/api/3/action/datastore_search'
    resource_id = '5fc13c50-b6f3-4712-b831-a75e0f91a17e'
    limit = 100000  # Number of rows to retrieve per request

    # Initialize an empty list to store the results
    results = []

    # Calculate the total number of requests needed
    total_rows = count
    total_requests = (total_rows // limit) + 1

    # Make multiple requests to retrieve all the rows
    for offset in range(0, total_requests * limit, limit):
        params = {'resource_id': resource_id, 'limit': limit, 'offset': offset}
        response = requests.get(url, params=params).json()
        data = response['result']['records']
        results.extend(data)

    # Create a DataFrame from the combined results
    df = pd.DataFrame(results)

    # THIRD PART OF UPDATE - ADDING VARIABLES TO THE DATAFRAME
    # make 'year' and 'quarter' variable
    df['year'] = df['Quarter'].str[0:4]
    df['quarter'] = df['Quarter'].str[5:]

    #  Making the various "other" statistical crime groups into "אחר"
    other_list = (df['StatisticCrimeGroup'].unique()[9:12])
    df['StatisticCrimeGroup'] = df['StatisticCrimeGroup'].apply(lambda x: 'אחר' if x in other_list else x)

    # making column with city code matching the CBS
    df['city_code'] = (df['Settlement_Council'].map(
        df_symbol.set_index('Settlement_Council')['city_code'])).astype(str)
    # making column with city type - 1=jewish, 2=mixed, 3=arab
    df['city_type'] = df['Settlement_Council'].map(
        df_symbol.set_index('Settlement_Council')['city_type'])
    # making column with percentage of population aged 15-29
    df['youth'] = df['Settlement_Council'].map(
        df_symbol.set_index('Settlement_Council')['youth'])
    df['population'] = df['Settlement_Council'].map(
        df_symbol.set_index('Settlement_Council')['population'])

    # Making dataframe with police city names and CBS city codes - for future use
    df_city_code = df[['city_code', 'Settlement_Council']]

    # save to local csv file
    df.to_csv('output.csv')
    df_city_code.to_csv('city_code_dataframe.csv')