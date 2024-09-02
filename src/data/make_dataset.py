import pandas as pd

df = pd.read_csv(r"C:\Users\kugor\repos\Coursera_Streamlit_Project_2_Dashboards\data\raw\Tweets.csv")

rows = df.shape[0]
ids = []

for i in range(rows):
    id = i+1
    ids.append(id)


len(ids) == rows

df['tweet_id'] = ids
df.set_index("tweet_id", inplace=True)

df.to_pickle("data/interim/tweets_processed.pkl")

df_no_nas = df.dropna(axis=1)

df_no_nas.to_pickle("data/interim/tweets_no_nas.pkl")