import pandas as pd
import streamlit as st
import altair as alt
from dataframemaker import df, df_quarter, latest_year, latest_quarter


def national_data(crimegroup, crimetype, window_width):
    st.write("""
        ### Nationwide Data
        """)

    # Setting the number of columns according to width of window being used
    if window_width <= 600:
        ncol = 1
    elif 600 < window_width <= 1100:
        ncol = 2
    elif window_width > 1100:
        ncol = 3

    # The graph functions

    # ANNUAL TOTAL DATA NATIONWIDE
    def national1():
        st.markdown("""
        Total cases by **year**
        """)
        try:
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

    # QUARTERLY TOTAL DATA NATIONWIDE
    def national2():
        st.markdown("""
        Total cases by **quarter**
        """)
        try:
            # Defining the data for the chart of quarterly tikim
            total = pd.DataFrame({'y': list(df.groupby(df['Quarter'])['TikimSum'].sum().values),
                                  'x': list(sorted(df['Quarter'].unique()))
                                  })
            y_max = 1.05 * max(list(df.groupby(df['Quarter'])['TikimSum'].sum().values))
            y_min = 0.95 * min(list(df.groupby(df['Quarter'])['TikimSum'].sum().values))

            # Defining the chart
            chart = alt.Chart(total).mark_bar(size=window_width * 0.005, color='orange').encode(
                x=alt.X('x', axis=alt.Axis(title='Quarter', labelFontSize=8)),
                y=alt.Y('y', axis=alt.Axis(title='cases'), scale=alt.Scale(domain=(y_min, y_max), clamp=True), ))
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    # LATEST QUARTER CRIMES BY GROUP OF TYPES OF CRIME
    def national3():
        st.write(f"""
        Total cases by crime group: **{latest_quarter} {latest_year}**  
            """)
        try:
            # Choosing only data for latest available quarter
            dfi = df.loc[(df['year'] == latest_year) & (df['quarter'] == latest_quarter)]
            total = pd.DataFrame({'category': dfi['StatisticCrimeGroup'].unique().tolist()[1:],
                                  'value': dfi.groupby(dfi['StatisticCrimeGroup'])['TikimSum'].sum().values
                                  })
            chart = alt.Chart(total).mark_arc(innerRadius=window_width * 0.05).encode(
                theta='value',
                color=alt.Color('category:N', scale=alt.Scale(scheme='category10')),
            )
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write('**NO DATA**')

    def national4():
        st.markdown("""
        Total cases by year (**same period**)
        """)
        try:
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

    # Total category of crime by quarter
    def national5():
        try:
            st.markdown(f"""
            **{crimegroup}** by quarter
            """)
            # Defining the data for the chart of annual tikim
            dfi = df.loc[df['StatisticCrimeGroup'] == f'{crimegroup}']
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
            st.write(' **NO DATA**')

    # Total category of crime by quarter
    def national6():
        try:
            st.markdown(f"""
            **{crimetype}** by quarter
            """)
            # Defining the data for the chart of annual tikim
            dfi = df.loc[df['StatisticCrimeType'] == f'{crimetype}']
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

    def national7():
        try:
            st.markdown("""
                        **Percent of cases in **arab municipalities** by quarter**
                        """)
            # Defining the data for the chart of annual tikim
            the_nums = df.groupby(['Quarter', 'city_type'])['TikimSum'].sum().values
            arab = []
            for i in range(0, int(len(the_nums)), 3):
                percent = f'{((the_nums[i + 1] / (the_nums[i] + the_nums[i + 1] + the_nums[i + 2])) * 100):.2f}'
                arab.append(percent)
            total = pd.DataFrame({'y': arab,
                                  'x': (sorted(df['Quarter'].unique().tolist()))
                                  })
            total['x'] = total['x'].astype(str)
            # Defining the chart
            chart = alt.Chart(total).mark_line(strokeWidth=5, color='green').encode(
                x=alt.X('x', axis=alt.Axis(title='quarter')),
                y=alt.Y('y', axis=alt.Axis(title='Percent')), )
            # Rendering the chart
            st.altair_chart(chart, use_container_width=True)
        except:
            st.write(' **NO DATA**')

    # Making the columns
    cols = st.columns(ncol)
    # Making list of the graph functions
    functions = [national1, national2, national3, national4,
                 national5, national6, national7]

    # Putting the graphs in the right columns
    num_functions = len(functions)

    column_index = 0
    col_list = st.columns(ncol)

    for i in range(num_functions):
        column_index = i % ncol

        with col_list[column_index]:
            functions[i]()
