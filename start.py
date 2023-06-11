import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
from dataframemaker import df, df_quarter, latest_year, latest_quarter

def start_data(window_width):
    st.write("""
    ### The data at a glance
    """)

    # Setting the number of columns according to width of window being used
    if window_width <= 600:
        ncol = 1
    elif 600 < window_width <= 1100:
        ncol = 2
    elif window_width > 1100:
        ncol = 3

    # The graph functions
    def start1():
        try:
            st.markdown("""
            **Total cases by year**
            """)
            # Defining the data for the chart of annual tikim
            total = pd.DataFrame({'y': list(df.groupby(df['year'])['TikimSum'].sum().values),
                                  'x': (sorted(df['year'].unique().tolist()))
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

    def start2():
        try:
            st.markdown(f"""
            **Total cases by Police district: {latest_quarter} {latest_year}**
            """)
            # Defining the data for the chart of annual tikim
            dfi = df.loc[(df['year'] == latest_year) & (df['quarter'] == latest_quarter)]
            total = pd.DataFrame({'y': list(dfi.groupby(dfi['PoliceDistrict'])['TikimSum'].sum().values),
                                  'x': (sorted(dfi['PoliceDistrict'].unique().tolist()))
                                  })
            # Defining the chart
            chart = alt.Chart(total).mark_bar(size=window_width * 0.025, color='orange').encode(
                x=alt.X('x', axis=alt.Axis(title='year')),
                y=alt.Y('y', axis=alt.Axis(title='cases')), )
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    def start3():
        try:
            st.write(f"""
            **Total cases by type of municipality: {latest_quarter} {latest_year}**  
                """)
            # Choosing only data for latest available quarter
            dfi = df.loc[(df['year'] == latest_year) & (df['quarter'] == latest_quarter)]
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

    def start4():
        try:
            st.markdown("""
            **Total cases by year (same period)**
            """)
            # Defining the data for the chart of annual tikim
            total = pd.DataFrame({'y': list(df_quarter.groupby(df_quarter['year'])['TikimSum'].sum().values),
                                  'x': (sorted(df_quarter['year'].unique().tolist()))
                                  })
            total['x'] = total['x'].astype(str)
            y_max = 1.05 * max(list(df.groupby(df_quarter['year'])['TikimSum'].sum().values))
            y_min = 0.95 * min(list(df.groupby(df_quarter['year'])['TikimSum'].sum().values))
            # Defining the chart
            chart = alt.Chart(total).mark_bar(size=window_width * 0.025).encode(
                x=alt.X('x', axis=alt.Axis(title='year')),
                y=alt.Y('y', axis=alt.Axis(title='cases'), scale=alt.Scale(domain=(y_min, y_max), clamp=True)), )
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    def start5():
        try:
            st.markdown("""
            **Total murders by quarter**
            """)
            # Defining the data for the chart of annual tikim
            dfi = df.loc[df['StatisticCrimeType'] == 'רצח']
            total = pd.DataFrame({'y': list(dfi.groupby(df['Quarter'])['TikimSum'].sum().values),
                                  'x': (sorted(dfi['Quarter'].unique().tolist()))
                                  })
            total['x'] = total['x'].astype(str)
            # Defining the chart
            chart = alt.Chart(total).mark_line(strokeWidth=3, color='red').encode(
                x=alt.X('x', axis=alt.Axis(title='quarter')),
                y=alt.Y('y', axis=alt.Axis(title='cases')), )
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    def start6():
        try:
            st.markdown("""
            **Total car thefts by quarter**
            """)
            # Defining the data for the chart of annual tikim
            dfi = df.loc[df['StatisticCrimeType'] == 'גניבה שמוש רכב ללא רשות']
            total = pd.DataFrame({'y': list(dfi.groupby(df['Quarter'])['TikimSum'].sum().values),
                                  'x': (sorted(dfi['Quarter'].unique().tolist()))
                                  })
            total['x'] = total['x'].astype(str)
            # Defining the chart
            chart = alt.Chart(total).mark_line(strokeWidth=3).encode(
                x=alt.X('x', axis=alt.Axis(title='quarter')),
                y=alt.Y('y', axis=alt.Axis(title='cases')), )
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write(' **NO DATA**')

    # Making the columns
    cols = st.columns(ncol)
    # Making list of the graph functions
    functions = [start1, start2, start3, start4, start5, start6]

    num_functions = len(functions)

    column_index = 0
    col_list = st.columns(ncol)

    for i in range(num_functions):
        column_index = i % ncol

        with col_list[column_index]:
            functions[i]()
