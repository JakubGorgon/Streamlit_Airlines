import pandas as pd; import numpy as np
from matplotlib import pyplot as plt; import seaborn as sns
import streamlit as st

st.set_page_config(layout="wide")

df_raw = pd.read_pickle("data/interim/tweets_processed.pkl")
df = pd.read_pickle("data/interim/tweets_no_nas.pkl")

st.title(":blue[**Sentiment Analysis of \
         Tweets About US Airlines**] 🐦")

if st.sidebar.checkbox("Show Sample of Raw Data"):
    st.subheader("Raw Data")
    st.dataframe(df_raw.sample(10))

if st.sidebar.checkbox("Show Sample of Data Without Missing Values"):
    st.subheader("Data without Missing Values")
    st.dataframe(df.sample(10))

