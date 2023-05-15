import pandas as pd
import streamlit as st

st.write("""
# govgr web scraping app
""")

# read df from github
github_data_path = "https://raw.githubusercontent.com/Giovalentini/govgr/main/"
df = pd.read_csv(github_data_path + 'govgr_data.csv')

# show df in app
st.dataframe(df)
