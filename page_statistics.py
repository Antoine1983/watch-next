import streamlit as st
import matplotlib.pyplot as plt
import data_api

@st.cache_data
def load_good_movies():
    return data_api.load_good_movies()

movies = load_good_movies()

st.title("Statistics")

fig, ax = plt.subplots()
ax.hist(movies['startYear'], bins=12)

st.pyplot(fig)
