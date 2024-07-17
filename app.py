import streamlit as st
import pandas as pd


try:
    df = pd.read_excel('rawdata.xlsx')
except FileNotFoundError:
    st.error("File not found. Please check the path to your Excel file.")

if 'date' in df.columns and 'time' in df.columns:
    df['date'] = df['date'].astype(str)
    df['time'] = df['time'].astype(str)

    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

    df['date'] = df['datetime'].dt.date

    def calculate_datewise_totals(data):
        # Datewise total duration for each location (inside and outside)
        location_summary = data.groupby(['date', 'location']).size().unstack(fill_value=0).reset_index()

        # Datewise number of picking and placing activities
        activity_summary = data.groupby(['date', 'activity']).size().unstack(fill_value=0).reset_index()

        return location_summary, activity_summary

    # Calculate datewise totals
    location_summary, activity_summary = calculate_datewise_totals(df)

    # Streamlit app
    st.title('Activity Analysis')
    st.header('Datewise Total Duration and Activity Counts')

    # Display datewise totals for inside and outside
    st.subheader('Datewise Total Duration for Each Inside and Outside')
    st.write(location_summary)

    # Display datewise totals for picking and placing activities
    st.subheader('Datewise Number of Picking and Placing Activities')
    st.write(activity_summary)

    # Display the raw data
    st.subheader('Raw Data')
    st.write(df.head())
else:
    st.warning("Ensure that your dataset contains columns 'date' and 'time'.")

# To run the Streamlit app, save this script as `streamlit_app.py` and run the following command:
# streamlit run streamlit_app.py
