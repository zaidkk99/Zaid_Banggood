import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pyodbc
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine
import urllib
import sqlite3

st.set_page_config(layout="wide") 

connection = sqlite3.connect("bangGoodDB.db")
table_name = "product_listings"

def runDbQuery(query):
    result = pd.read_sql(query, connection)
    return result

st.title("BangGood")
st.subheader("This dashboard show analysis of data from BangGood", divider="gray")

st.markdown(
    f"""
    <div style='padding: 10px 0;'></div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)
with col1:
    #Analysis 1: Number of card avalible in each city:
    
    st.markdown(
    f"""
    <h4 style='font-size:24px; font-weight:700; padding: 0;'>
        Total Number of Listings
    </h4>
    """,
    unsafe_allow_html=True
    )
    
    listing_count = runDbQuery(f"SELECT COUNT(*) AS TOTAL_COUNT FROM {table_name};")
    
    st.markdown(
    f"""
    <h3 style='font-size:36px; font-weight:700; padding: 0;'>
        {listing_count["TOTAL_COUNT"][0]}
    </h3>
    """,
    unsafe_allow_html=True
    )

with col2:
    st.markdown(
    f"""
    <h4 style='font-size:24px; font-weight:700; padding: 0;'>
        Average price of available product
    </h4>
    """,
    unsafe_allow_html=True
    )
    
    average_price = runDbQuery(f" SELECT ROUND(AVG(Price), 2) AS AVERAGE_PRICE FROM {table_name};")
    
    st.markdown(
    f"""
    <h3 style='font-size:36px; font-weight:700; padding: 0;'>
        {average_price["AVERAGE_PRICE"][0]}
    </h3>
    """,
    unsafe_allow_html=True
    )
    
with col3:

    st.markdown(
    f"""
    <h4 style='font-size:24px; font-weight:700; padding: 0;'>
        Average rating of available product
    </h4>
    """,
    unsafe_allow_html=True
    )
    
    average_rating = runDbQuery(f"SELECT ROUND(AVG(Rating), 2) AS AVERAGE_RATING FROM {table_name};")
    
    st.markdown(
    f"""
    <h3 style='font-size:36px; font-weight:700; padding: 0;'>
        {average_rating["AVERAGE_RATING"][0]}
    </h3>
    """,
    unsafe_allow_html=True
    )

st.markdown(
    f"""
    <div style='padding: 20px 0;'></div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)
with col1:
    query_1 = runDbQuery(f" SELECT Category, COUNT(*) AS CountPerCategory FROM {table_name} GROUP BY Category ORDER BY CountPerCategory DESC;")
    
    query_1_x = query_1['Category']
    query_1_y = query_1['CountPerCategory']

    # Create the Matplotlib figure and axes
    fig, ax = plt.subplots(figsize=(5, 5))

    # Plot the bar chart
    ax.bar(query_1_x, query_1_y, color='skyblue')
    ax.set_xlabel("Categories")
    ax.set_ylabel("Number of Product")
    ax.set_title("Number of Product in Each Category")
    ax.set_xticklabels(query_1_x, rotation=90, ha='right', fontsize=6)

    # Display the chart in Streamlit
    st.pyplot(fig)
    
with col2:
    query_2 = runDbQuery(f" SELECT Category, ROUND(AVG(Rating), 2) AS AverageRatingPerCategory FROM {table_name} GROUP BY Category ORDER BY AverageRatingPerCategory DESC;")
    
    query_2_x = query_2['Category']
    query_2_y = query_2['AverageRatingPerCategory']

    # Create the Matplotlib figure and axes
    fig2, ax2 = plt.subplots(figsize=(5, 5))

    # Plot the bar chart
    ax2.bar(query_2_x, query_2_y, color='skyblue')
    ax2.set_xlabel("Categories")
    ax2.set_ylabel("Rating")
    ax2.set_title("Average Rating Each Category")
    ax2.set_xticklabels(query_2_x, rotation=90, ha='right', fontsize=6)

    # Display the chart in Streamlit
    st.pyplot(fig2)

st.markdown(
    f"""
    <div style='padding: 10px 0;'></div>
    """,
    unsafe_allow_html=True
)

all_listing = runDbQuery(f"SELECT * FROM {table_name};")
total_listings = len(all_listing)

st.markdown(
    f"""
    <p style='font-size: 22px; font-weigh: 600; padding-top: 20px;'>List of {total_listings} products available:</p>
    """,
    unsafe_allow_html=True
)
st.dataframe(all_listing)

st.markdown(
    f"""
    <div style='padding: 10px 0;'></div>
    """,
    unsafe_allow_html=True
)

