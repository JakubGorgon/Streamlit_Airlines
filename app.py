import pandas as pd; import numpy as np
from matplotlib import pyplot as plt; import seaborn as sns
import streamlit as st
import plotly.express as px

# st.set_page_config(layout="wide")

@st.cache_data(persist=True)
def load_data():
    df_raw = pd.read_pickle("data/interim/tweets_processed.pkl")
    df = pd.read_pickle("data/interim/tweets_no_nas.pkl")
    return df_raw, df

df_raw, df = load_data()

st.markdown(
    """
    <style>
    .title {
        font-size: 50px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        text-shadow: 2px 2px #ffffff;
    }
    .emoji {
        font-size: 40px;
    }
    </style>
    <p class="title">Sentiment Analysis of Tweets About US Airlines <span class="emoji">🐦</span></p>
    """,
    unsafe_allow_html=True
)



st.sidebar.subheader("Example Random Tweet")
sentiments = tuple(df['airline_sentiment'].unique())
sentiment = st.sidebar.selectbox(label="Sentiment", 
                                 options=sentiments, 
                                 placeholder="Choose to See an Example",
                                 key='s')

# Check if the sentiment is not in session state
if sentiment not in st.session_state:
    filt = df['airline_sentiment'] == sentiment
    df_filt = df[filt]

    # Use the retweet_count column as weights for sampling
    random_tweet = df_filt[['text', 'retweet_count']].sample(
        weights=df_filt['retweet_count'] + 1,  # Add 1 to avoid zero weights
        n=1
    ).iloc[0, 0:2]
    
    st.session_state[sentiment] = [
        random_tweet.iloc[0],  # Tweet text
        str(random_tweet.iloc[1])  # Retweet count
    ]

# Concatenate tweet text and retweet count
tweet_text = st.session_state[sentiment][0]
retweet_count = st.session_state[sentiment][1]
formatted_tweet = f"Tweet: {tweet_text}\n\nRetweets: {retweet_count}"

# Display the formatted tweet in the sidebar
st.sidebar.write(formatted_tweet)

chart_options = ("Bar Chart", "Pie Chart")
st.sidebar.subheader("Visualisation to Plot")
plots = st.sidebar.selectbox("Visualisation Type", 
                               chart_options,
                               key='p')

sentiment_series = df['airline_sentiment'].value_counts()
names = sentiment_series.index
counts = sentiment_series.values

custom_colors = ['#EF553B', '#636EFA', '#00CC96'] 

if not st.sidebar.checkbox("Hide", True):
    if "Pie Chart" in plots:
        fig = px.pie(data_frame=sentiment_series,
                    values=counts,
                    names=names,
                    color_discrete_sequence=custom_colors,
                    title="Distribution of Tweets by Sentiment",
                    labels={"airline_sentiment":"Tweet Sentiment"}
                    )
        # st.subheader("Distribution of Tweets by Sentiment")
        st.plotly_chart(fig)

    if "Bar Chart" in plots:
        fig = px.bar(data_frame=sentiment_series,
                    y = counts,
                    x = names,
                    title = "Distribution of Tweets by Sentiment",
                    color=names,
                    color_discrete_sequence=custom_colors,
                    labels={'airline_sentiment': 'Tweet Sentiment', 
                            'y': 'Number of Tweets'}
                    )
        st.plotly_chart(fig)


st.write(df['latitude'])







df.groupby(by='airline')['airline_sentiment'].value_counts()



# if st.sidebar.checkbox("Show Sample of Raw Data"):
#     st.subheader("Raw Data")
#     st.dataframe(df_raw.sample(10))

# if st.sidebar.checkbox("Show Sample of Data Without Missing Values"):
#     st.subheader("Data without Missing Values")
#     st.dataframe(df.sample(10))

