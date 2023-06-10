import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
from dataframemaker import df, df_quarter, latest_year, latest_quarter


def start_data(window_width):
    st.write("""
    ### The data at a glance
    """)
    # Making three columns
    col1, col2, col3 = st.columns(3)
    # ANNUAL TOTAL DATA NATIONWIDE
    with col1:
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
            chart = alt.Chart(total).mark_bar(size=window_width*0.025).encode(
                x=alt.X('x', axis=alt.Axis(title='year')),
                y=alt.Y('y', axis=alt.Axis(title='cases')),)
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    with col2:
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
            chart = alt.Chart(total).mark_bar(size=window_width*0.025, color='orange').encode(
                x=alt.X('x', axis=alt.Axis(title='year')),
                y=alt.Y('y', axis=alt.Axis(title='cases')),)
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')


    # LATEST QUARTER CRIMES BY TYPE OF MUICIPALITY
    with col3:
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
            chart = alt.Chart(total).mark_arc(innerRadius=window_width*0.05).encode(
                theta='value',
                color=alt.Color('category:N', scale=alt.Scale(scheme='category10')),
            )
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    with col1:
        try:
            st.markdown("""
            **Total cases by year (same period)**
            """)
            # Defining the data for the chart of annual tikim
            total = pd.DataFrame({'y': list(df_quarter.groupby(df_quarter['year'])['TikimSum'].sum().values),
                                  'x': (sorted(df_quarter['year'].unique().tolist()))
                                  })
            total['x'] = total['x'].astype(str)
            y_max = 1.05*max(list(df.groupby(df_quarter['year'])['TikimSum'].sum().values))
            y_min = 0.95*min(list(df.groupby(df_quarter['year'])['TikimSum'].sum().values))
            # Defining the chart
            chart = alt.Chart(total).mark_bar(size=window_width*0.025).encode(
                x=alt.X('x', axis=alt.Axis(title='year')),
                y=alt.Y('y', axis=alt.Axis(title='cases'), scale=alt.Scale(domain=(y_min, y_max), clamp=True)), )
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    # Total murders by quarter
    with col2:
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

    # Total car thefts by quarter
    with col3:
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

