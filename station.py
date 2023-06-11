import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from dataframemaker import df, df_quarter, latest_year, latest_quarter


def station_data(tachana, crimegroup3, crimetype3, window_width):
    st.write(f"""
            ### Station Data: {tachana}
            """)

    # Setting the number of columns according to width of window being used
    if window_width <= 600:
        ncol = 1
    elif 600 < window_width <= 1100:
        ncol = 2
    elif window_width > 1100:
        ncol = 3

    # The graph functions

    def station1():
        st.markdown(f"""
        Total cases by year for: **{tachana}**
        """)
        try:
            # Defining the data for the chart of quarterly tikim
            dfi = df.loc[df['PoliceStation'] == f'{tachana}']
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

    def station2():
        st.markdown(f"""
        Total cases by quarter for: **{tachana}**
        """)
        try:
            # Defining the data for the chart of quarterly tikim
            dfi = df.loc[df['PoliceStation'] == f'{tachana}']
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

    def station3():
        st.write(f"""
        Total cases by type of municipality: **{latest_quarter} {latest_year} {tachana}**  
            """)
        try:
            # Choosing only data for latest available quarter
            dfi = df.loc[(df['year'] == latest_year) & (df['quarter'] == latest_quarter) &
                         (df['PoliceStation'] == f'{tachana}')]
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

    def station4():
        st.markdown(f"""
        Total cases by year (**same period**) for: **{tachana}**
        """)
        try:
            # Defining the data for the chart of annual tikim
            dfi = df_quarter.loc[df['PoliceStation'] == f'{tachana}']
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

    # Total category of crime by quarter
    def station5():
        st.markdown(f"""
        **{crimegroup3}** by quarter **{tachana}**
        """)
        try:
            # Defining the data for the chart of annual tikim
            dfi = df.loc[(df['PoliceStation'] == f'{tachana}') &
                         (df['StatisticCrimeGroup'] == f'{crimegroup3}')]
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
    def station6():
        st.markdown(f"""
        **{crimetype3}** by quarter **{tachana}**
        """)
        # Defining the data for the chart of annual tikim
        try:
            dfi = df.loc[(df['PoliceStation'] == f'{tachana}') &
                         (df['StatisticCrimeGroup'] == f'{crimegroup3}') &
                         (df['StatisticCrimeType'] == f'{crimetype3}')]
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
        functions = [station1, station2, station3, station4,
                     station5, station6]

        # Putting the graphs in the right columns
        num_functions = len(functions)

        column_index = 0
        col_list = st.columns(ncol)

        for i in range(num_functions):
            column_index = i % ncol

            with col_list[column_index]:
                functions[i]()
