import streamlit as st
from psycopg2 import sql
from sqlalchemy import create_engine
import pandas as pd
#from dotenv import load_dotenv
import os
import secrets

#Database connection
#load_dotenv()

#function to connect to database
def get_db_connection():

    #Database_URL = os.getenv('Database_URL_alpha')
    Database_URL = st.secrets['URL_Railway']
    engine= create_engine(Database_URL)
    return engine

#function to get bitcoin data from database
def fetch_bitcoin_data(engine):
    query = "SELECT * FROM bitcoin_prices ORDER BY date"
    df = pd.read_sql(query,engine)
    return df

def fetch_bitcoin_news(engine):
    query = "SELECT * FROM bitcoin_news"
    df = pd.read_sql(query,engine)
    return df

#get database connection
conn = get_db_connection()

#Fetch bitcoin data and news
bitcoin_data_df = fetch_bitcoin_data(conn)
bitcoin_news_df = fetch_bitcoin_news(conn)

# Dispay Bitcoin Data
st.title("Bitcoin Data")
st.line_chart(bitcoin_data_df.set_index('date')['close'])

#Display Bitcoin News
st.title("Bitcoin News")
st.write(bitcoin_news_df)