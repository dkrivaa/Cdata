import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from dataframemaker import df, df_quarter, latest_year, latest_quarter


def district_data(district, crimegroup1, crimetype1, window_width):
    st.write(f"""
        ### District Data: {district}
        """)

    # Setting the number of columns according to width of window being used
    if window_width <= 600:
        ncol = 1
    elif 600 < window_width <= 1100:
        ncol = 2
    elif window_width > 1100:
        ncol = 3

    # The graph functions
    def district1():
        st.markdown(f"""
                Total cases by year for: **{district}**
                """)
        try:
            # Defining the data for the chart of quarterly tikim
            dfi = df.loc[df['PoliceDistrict'] == district]
            total = pd.DataFrame({'y': list(dfi.groupby(dfi['year'])['TikimSum'].sum().values),
                                  'x': (sorted(dfi['year'].unique().tolist()))
                                  })
            total['x'] = total['x'].astype(str)
            # Defining the chart
            chart = alt.Chart(total).mark_bar(size=window_width * 0.025).encode(
                x=alt.X('x', axis=alt.Axis(title='year')),
                y=alt.Y('y', axis=alt.Axis(title='cases')), )
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    def district2():
        st.markdown(f"""
                Total cases by quarter for: **{district}**
                """)
        try:
            # Defining the data for the chart of quarterly tikim
            dfi = df.loc[df['PoliceDistrict'] == district]
            total = pd.DataFrame({'y': list(dfi.groupby(dfi['Quarter'])['TikimSum'].sum().values),
                                  'x': list(sorted(dfi['Quarter'].unique()))
                                  })
            y_max = 1.05 * max(list(dfi.groupby(dfi['Quarter'])['TikimSum'].sum().values))
            y_min = 0.9 * min(list(dfi.groupby(dfi['Quarter'])['TikimSum'].sum().values))
            # Defining the chart
            chart = alt.Chart(total).mark_bar(size=window_width * 0.005).encode(
                x=alt.X('x', axis=alt.Axis(title='Quarter', labelFontSize=8)),
                y=alt.Y('y', axis=alt.Axis(title='cases'), scale=alt.Scale(domain=(y_min, y_max), clamp=True), ))
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    def district3():
        st.write(f"""
                Total cases by type of municipality: **{latest_quarter} {latest_year}**  
                    """)
        try:
            # Choosing only data for latest available quarter
            dfi = df.loc[(df['year'] == latest_year) & (df['quarter'] == latest_quarter) &
                         (df['PoliceDistrict'] == f'{district}')]
            total = pd.DataFrame({'category': dfi['city_type'][~np.isnan(dfi['city_type'])].unique().tolist(),
                                  'value': dfi.groupby(dfi['city_type'])['TikimSum'].sum().values
                                  })
            # Revaluing the categories of types of municipalities
            total['category'] = total['category'].map(lambda x: 'Jewish' if x == 1
            else 'Mixed' if x == 2
            else 'Arab')
            chart = alt.Chart(total).mark_arc(innerRadius=window_width * 0.05).encode(
                theta='value',
                color=alt.Color('category:N', scale=alt.Scale(scheme='category10')),
            )
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    def district4():
        st.markdown(f"""
                Total cases by year (**same period**) for: **{district}**
                """)
        try:
            # Defining the data for the chart of annual tikim
            dfi = df_quarter.loc[df['PoliceDistrict'] == district]
            total = pd.DataFrame({'y': list(dfi.groupby(dfi['year'])['TikimSum'].sum().values),
                                  'x': (sorted(dfi['year'].unique().tolist()))
                                  })
            total['x'] = total['x'].astype(str)
            y_max = 1.05 * max(list(dfi.groupby(df_quarter['year'])['TikimSum'].sum().values))
            y_min = 0.95 * min(list(dfi.groupby(df_quarter['year'])['TikimSum'].sum().values))
            # Defining the chart
            chart = alt.Chart(total).mark_bar(size=window_width * 0.025).encode(
                x=alt.X('x', axis=alt.Axis(title='year')),
                y=alt.Y('y', axis=alt.Axis(title='cases'), scale=alt.Scale(domain=(y_min, y_max), clamp=True)), )
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    def district5():
        st.markdown(f"""
                Total cases by Police Region in: **{district}**
                """)
        try:
            dfi = df_quarter.loc[df['PoliceDistrict'] == district]
            dfs = dfi.loc[(dfi['year'] == latest_year) & (dfi['quarter'] == latest_quarter)]
            total = pd.DataFrame({'value': list(dfs.groupby(dfi['PoliceMerhav'])['TikimSum'].sum().values),
                                  'category': list(sorted(dfs['PoliceMerhav'].unique()))
                                  })
            chart = alt.Chart(total).mark_arc(innerRadius=window_width * 0.05).encode(
                theta='value',
                color=alt.Color('category:N', scale=alt.Scale(scheme='category10')),
            )
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    def district6():
        st.markdown(f"""
                Total cases by Police Stations in: **{district}**
                """)
        try:
            dfi = df_quarter.loc[df['PoliceDistrict'] == district]
            dfs = dfi.loc[(dfi['year'] == latest_year) & (dfi['quarter'] == latest_quarter)]
            total = pd.DataFrame({'y': list(dfs.groupby(dfi['PoliceStation'])['TikimSum'].sum().values),
                                  'x': list(sorted(dfs['PoliceStation'].unique()))
                                  })
            y_max = 1.05 * max(list(dfs.groupby(dfs['PoliceStation'])['TikimSum'].sum().values))
            y_min = 0.9 * min(list(dfs.groupby(dfs['PoliceStation'])['TikimSum'].sum().values))
            # Defining the chart
            chart = alt.Chart(total).mark_bar(size=window_width * 0.01, color='orange').encode(
                x=alt.X('x', axis=alt.Axis(title='Police Station', labelFontSize=12)),
                y=alt.Y('y', axis=alt.Axis(title='cases'), scale=alt.Scale(domain=(y_min, y_max), clamp=True), ))
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    def district7():
        st.markdown(f"""
                **{crimegroup1}** by quarter
                """)
        try:
            # Defining the data for the chart of annual tikim
            dfi = df.loc[(df['PoliceDistrict'] == f'{district}') &
                         (df['StatisticCrimeGroup'] == f'{crimegroup1}')]
            total = pd.DataFrame({'y': list(dfi.groupby(dfi['Quarter'])['TikimSum'].sum().values),
                                  'x': (sorted(dfi['Quarter'].unique().tolist()))
                                  })
            y_max = 1.05 * max(dfi.groupby(dfi['Quarter'])['TikimSum'].sum().values)
            y_min = 0.95 * min(dfi.groupby(dfi['Quarter'])['TikimSum'].sum().values)
            # Defining the chart
            chart = alt.Chart(total).mark_line(strokeWidth=5).encode(
                x=alt.X('x', axis=alt.Axis(title='quarter')),
                y=alt.Y('y', axis=alt.Axis(title='cases'), scale=alt.Scale(domain=(y_min, y_max), clamp=True)), )
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    def district8():
        st.markdown(f"""
                **{crimetype1}** by quarter
                """)
        try:
            # Defining the data for the chart of annual tikim
            dfi = df.loc[(df['PoliceDistrict'] == f'{district}') &
                         (df['StatisticCrimeGroup'] == f'{crimegroup1}') &
                         (df['StatisticCrimeType'] == f'{crimetype1}')]
            total = pd.DataFrame({'y': list(dfi.groupby(dfi['Quarter'])['TikimSum'].sum().values),
                                  'x': (sorted(dfi['Quarter'].unique().tolist()))
                                  })
            y_max = 1.05 * max(dfi.groupby(dfi['Quarter'])['TikimSum'].sum().values)
            y_min = 0.95 * min(dfi.groupby(dfi['Quarter'])['TikimSum'].sum().values)
            # Defining the chart
            chart = alt.Chart(total).mark_line(strokeWidth=2).encode(
                x=alt.X('x', axis=alt.Axis(title='quarter')),
                y=alt.Y('y', axis=alt.Axis(title='cases'), scale=alt.Scale(domain=(y_min, y_max), clamp=True)), )
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    # Making the columns
    cols = st.columns(ncol)
    # Making list of the graph functions
    functions = [district1, district2, district3, district4,
                 district5, district6, district7, district8]

    # Putting the graphs in the right columns
    num_functions = len(functions)

    column_index = 0
    col_list = st.columns(ncol)

    for i in range(num_functions):
        column_index = i % ncol

        with col_list[column_index]:
            functions[i]()



