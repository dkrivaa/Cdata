import streamlit as st
import streamlit_javascript as st_js

from dataframemaker import df, latest_year, latest_quarter

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
