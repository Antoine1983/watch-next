import streamlit as st
import matplotlib.pyplot as plt
import data_api

@st.cache_data
def load_good_movies():
    return data_api.load_good_movies()

movies = load_good_movies()

st.title("Statistics")

st.header("Distribution per average rating")

fig1, ax1 = plt.subplots()
ax1.hist(movies['averageRating'], bins=12)
st.pyplot(fig1)

st.header("Distribution per year")

fig2, ax2 = plt.subplots()
ax2.hist(movies['startYear'], bins=12)
st.pyplot(fig2)


st.header("Distribution per region")

fig3, ax3 = plt.subplots()
c = movies['country_region'].value_counts()
ax3.pie(c, labels=c.index)
st.pyplot(fig3)
