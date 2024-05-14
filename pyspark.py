import streamlit as st
import pandas as pd
import plotly.express as px
# from numerize.numerize import numerize 
from query import *  # Ensure this module contains relevant database query functions
from datetime import datetime

# Fetch data and create DataFrame
result = view_all_data()
df = pd.DataFrame(result, columns=['vendor', 'posted_on', 'job_title', 'job_location', 'category_skill', 'Employment_type'])
df['posted_on'] = pd.to_datetime(df['posted_on'].str.slice(0,10), errors='coerce')


# Setting up the date range selectors in the sidebar
today = datetime.today().date()  # Get today's date
startDate = df['posted_on'].min()
endDate = df['posted_on'].max()

# date1 = st.sidebar.date_input('Start Date', today, min_value=startDate, max_value=today)
# date2 = st.sidebar.date_input('End Date', today, min_value=startDate, max_value=endDate)

# # Filter data based on selected date range
# df = df[(df['posted_on'] >= date1) & (df['posted_on'] <= date2)]
col1,col2 = st.columns((2))
with col1:
    date1 = pd.to_datetime(st.date_input('Start Date',today, min_value=startDate, max_value=today))

with col2:
    date2 = pd.to_datetime(st.date_input('End Date',today, max_value=endDate))

df = df[(df['posted_on'] >= date1) & (df['posted_on'] <= date2)].copy()

# Sidebar filters
vendor = st.sidebar.multiselect('Select Vendor', options=df['vendor'].unique())
job_title = st.sidebar.multiselect('Select Job Title', options=df['job_title'].unique())

# Apply filters
if vendor:
    df = df[df['vendor'].isin(vendor)]
if job_title:
    df = df[df['job_title'].isin(job_title)]

# Display filtered data
st.dataframe(df)

# Grouped data for visualizations
vendor_df = df.groupby('vendor')['job_title'].count().reset_index()
job_df = df.groupby('job_title')['vendor'].count().reset_index()

# Visualization columns
col1, col2 = st.columns(2)

with col1:
    st.subheader('Vendor-wise Positions') 
    fig = px.bar(vendor_df, x='vendor', y='job_title', template='seaborn')
    st.plotly_chart(fig, use_container_width=True)

    fig1 = px.pie(vendor_df, values='job_title', names='vendor', hole=0.5)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader('Job Title-wise Positions') 
    fig = px.bar(job_df, x='job_title', y='vendor', template='seaborn')
    st.plotly_chart(fig, use_container_width=True)

    fig1 = px.pie(job_df, values='vendor', names='job_title', hole=0.5)
    st.plotly_chart(fig1, use_container_width=True)
