import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from dataframemaker import df, df_quarter, latest_year, latest_quarter


def region_data(region, crimegroup2, crimetype2, window_width):
    st.write(f"""
            ### Region Data: {region}
            """)

    # Setting the number of columns according to width of window being used
    if window_width <= 600:
        ncol = 1
    elif 600 < window_width <= 1100:
        ncol = 2
    elif window_width > 1100:
        ncol = 3

    # The graph functions

    def region1():
        st.markdown(f"""
        Total cases by year for: **{region}**
        """)
        try:
            # Defining the data for the chart of quarterly tikim
            dfi = df.loc[df['PoliceMerhav'] == f'{region}']
            total = pd.DataFrame({'y': list(dfi.groupby(dfi['year'])['TikimSum'].sum().values),
                                  'x': (sorted(dfi['year'].unique().tolist()))
                                  })
            total['x'] = total['x'].astype(str)
            # Defining the chart
            chart = alt.Chart(total).mark_bar(size=window_width*0.025).encode(
                x=alt.X('x', axis=alt.Axis(title='year')),
                y=alt.Y('y', axis=alt.Axis(title='cases')), )
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    def region2():
        st.markdown(f"""
        Total cases by quarter for: **{region}**
        """)
        try:
            # Defining the data for the chart of quarterly tikim
            dfi = df.loc[df['PoliceMerhav'] == f'{region}']
            total = pd.DataFrame({'y': list(dfi.groupby(dfi['Quarter'])['TikimSum'].sum().values),
                                  'x': list(sorted(dfi['Quarter'].unique()))
                                  })
            y_max = 1.05 * max(list(dfi.groupby(dfi['Quarter'])['TikimSum'].sum().values))
            y_min = 0.9 * min(list(dfi.groupby(dfi['Quarter'])['TikimSum'].sum().values))
            # Defining the chart
            chart = alt.Chart(total).mark_bar(size=window_width*0.005, color='orange').encode(
                x=alt.X('x', axis=alt.Axis(title='Quarter', labelFontSize=8)),
                y=alt.Y('y', axis=alt.Axis(title='cases'), scale=alt.Scale(domain=(y_min, y_max), clamp=True), ))
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    # TIKIM FOR POLICE STATIONS IN SPECIFIED REGION
    def region3():
        st.markdown(f"""
            Total cases by Police stations in: **{region}**
            """)
        try:
            dfi = df.loc[df['PoliceMerhav'] == f'{region}']
            dfs = dfi.loc[(dfi['year'] == latest_year) & (dfi['quarter'] == latest_quarter)]
            total = pd.DataFrame({'value': list(dfs.groupby(dfi['PoliceStation'])['TikimSum'].sum().values),
                                  'category': list(sorted(dfs['PoliceStation'].unique()))
                                  })
            chart = alt.Chart(total).mark_arc(innerRadius=window_width*0.05).encode(
                theta='value',
                color=alt.Color('category:N', scale=alt.Scale(scheme='category10')),
            )
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    def region4():
        st.markdown(f"""
        Total cases by year (**same period**) for: **{region}**
        """)
        try:
            # Defining the data for the chart of annual tikim
            dfi = df_quarter.loc[df['PoliceMerhav'] == f'{region}']
            total = pd.DataFrame({'y': list(dfi.groupby(dfi['year'])['TikimSum'].sum().values),
                                  'x': (sorted(dfi['year'].unique().tolist()))
                                  })
            total['x'] = total['x'].astype(str)
            y_max = 1.05 * max(list(dfi.groupby(df_quarter['year'])['TikimSum'].sum().values))
            y_min = 0.95 * min(list(dfi.groupby(df_quarter['year'])['TikimSum'].sum().values))
            # Defining the chart
            chart = alt.Chart(total).mark_bar(size=window_width*0.025).encode(
                x=alt.X('x', axis=alt.Axis(title='year')),
                y=alt.Y('y', axis=alt.Axis(title='cases'), scale=alt.Scale(domain=(y_min, y_max), clamp=True)), )
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    def region5():
        st.write(f"""
        Total cases by type of municipality: **{latest_quarter} {latest_year} {region}**  
            """)
        try:
            # Choosing only data for latest available quarter
            dfi = df.loc[(df['year'] == latest_year) & (df['quarter'] == latest_quarter) &
                         (df['PoliceMerhav'] == f'{region}')]
            total = pd.DataFrame({'category': dfi['city_type'][~np.isnan(dfi['city_type'])].unique().tolist(),
                                  'value': dfi.groupby(dfi['city_type'])['TikimSum'].sum().values
                                  })
            # Revaluing the categories of types of municipalities
            total['category'] = total['category'].map(lambda x: 'Jewish' if x == 1
                                                                else 'Mixed' if x == 2
                                                                else 'Arab')
            chart = alt.Chart(total).mark_arc(innerRadius=window_width*0.05).encode(
                theta='value',
                color=alt.Color('category:N', scale=alt.Scale(scheme='category10')),
            )
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    # Total category of crime by quarter
    def region6():
        st.markdown(f"""
        **{crimegroup2}** by quarter **{region}**
        """)
        try:
            # Defining the data for the chart of annual tikim
            dfi = df.loc[(df['PoliceMerhav'] == f'{region}') &
                         (df['StatisticCrimeGroup'] == f'{crimegroup2}')]
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

    # Total category of crime by quarter
    def region7():
        st.markdown(f"""
        **{crimetype2}** by quarter **{region}**
        """)
        # Defining the data for the chart of annual tikim
        try:
            dfi = df.loc[(df['PoliceMerhav'] == f'{region}') &
                         (df['StatisticCrimeGroup'] == f'{crimegroup2}') &
                         (df['StatisticCrimeType'] == f'{crimetype2}')]
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
            st.write(' **NO DATA**')


    # Making the columns
    cols = st.columns(ncol)
    # Making list of the graph functions
    functions = [region1, region2, region3, region4,
                 region5, region6, region7]

    # Putting the graphs in the right columns
    num_functions = len(functions)

    column_index = 0
    col_list = st.columns(ncol)

    for i in range(num_functions):
        column_index = i % ncol

        with col_list[column_index]:
            functions[i]()
