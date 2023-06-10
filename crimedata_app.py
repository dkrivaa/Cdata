import streamlit as st
import streamlit_javascript as st_js

from dataframemaker import df, latest_year, latest_quarter
import start
import national
import district
import region
import station
import municipal

# Set the page layout to wide
st.set_page_config(layout="wide")
window_width = st_js.st_javascript('window.innerWidth')

st.write(f'{window_width}')
# MAIN DISPLAY AT STARTUP
st.write(f"""
# Crime Data App
An **interactive visualization** of official police crime data as published every quarter.
Latest available data: **{latest_quarter} {latest_year}**.
""") #

st.markdown("<hr>", unsafe_allow_html=True)

# SIDEBAR
st.sidebar.title('EXPLORE THE DATA')


level1 = st.sidebar.selectbox('**What would You like to explore**', ['Data at a Glance',
                                                                    'Nationwide data',
                                                                    'Police District data',
                                                                    'Police Region data',
                                                                    'Police station data',
                                                                    'municipality data',
                                                                    ])

if level1 == 'Data at a Glance':
    # FOR STARTUP
    start.start_data(window_width)

elif level1 == 'Nationwide data':
    crimegroup = st.sidebar.selectbox('**Choose Crime category**',
                                        sorted(df['StatisticCrimeGroup'].unique()[1:],
                                        reverse=True), index=8)
    dfi = df.loc[df['StatisticCrimeGroup'] == f'{crimegroup}']
    crimetype = st.sidebar.selectbox('**Choose specific crime**',
                                     dfi['StatisticCrimeType'].unique()[1:], index=1)
    national.national_data(crimegroup, crimetype, window_width)

elif level1 == 'Police District data':
    machoz = st.sidebar.selectbox('**Choose Police District**', df['PoliceDistrict'].unique())
    crimegroup1 = st.sidebar.selectbox('**Choose Crime category**',
                                      sorted(df['StatisticCrimeGroup'].unique()[1:],
                                             reverse=True), index=8)
    dfi = df.loc[df['StatisticCrimeGroup'] == f'{crimegroup1}']
    crimetype1 = st.sidebar.selectbox('**Choose specific crime**',
                                     dfi['StatisticCrimeType'].unique()[1:], index=1)
    district.district_data(machoz, crimegroup1, crimetype1, window_width)

elif level1 == 'Police Region data':
    merchav = st.sidebar.selectbox('**Choose Police Region**', df['PoliceMerhav'].unique())
    crimegroup2 = st.sidebar.selectbox('**Choose Crime category**',
                                       sorted(df['StatisticCrimeGroup'].unique()[1:],
                                              reverse=True), index=8)
    dfi = df.loc[df['StatisticCrimeGroup'] == f'{crimegroup2}']
    crimetype2 = st.sidebar.selectbox('**Choose specific crime**',
                                      dfi['StatisticCrimeType'].unique()[1:], index=1)
    region.region_data(merchav, crimegroup2, crimetype2, window_width)

elif level1 == 'Police station data':
    tachana = st.sidebar.selectbox('**Choose Police station**', df['PoliceStation'].unique())
    crimegroup3 = st.sidebar.selectbox('**Choose Crime category**',
                                       sorted(df['StatisticCrimeGroup'].unique()[1:],
                                              reverse=True), index=8)
    dfi = df.loc[df['StatisticCrimeGroup'] == f'{crimegroup3}']
    crimetype3 = st.sidebar.selectbox('**Choose specific crime**',
                                      dfi['StatisticCrimeType'].unique()[1:], index=1)
    station.station_data(tachana, crimegroup3, crimetype3, window_width)

elif level1 == 'municipality data':
    muni = st.sidebar.selectbox('**Choose Municipality**', df['Settlement_Council'].unique()[1:])
    crimegroup4 = st.sidebar.selectbox('**Choose Crime category**',
                                       sorted(df['StatisticCrimeGroup'].unique()[1:],
                                              reverse=True), index=8)
    dfi = df.loc[df['StatisticCrimeGroup'] == f'{crimegroup4}']
    crimetype4 = st.sidebar.selectbox('**Choose specific crime**',
                                      dfi['StatisticCrimeType'].unique()[1:], index=1)
    municipal.muni_data(muni, crimegroup4, crimetype4, window_width)
