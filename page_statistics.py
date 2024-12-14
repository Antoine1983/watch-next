import streamlit as st
import data_api

@st.cache_data
def load_good_movies():
    return data_api.load_good_movies()

movies = load_good_movies()

display_columns = [
    'primaryTitle',
    'averageRating',
    'numVotes',
    'startYear'
]

best_movies = movies[display_columns].loc[movies['numVotes'] > 10 ** 6].sort_values(by='averageRating', ascending=False).head(10)

st.header('Best movies')

st.dataframe(best_movies, hide_index=True)

st.caption('Top 10 movies with at least 1 million votes ranked by average rating.')

# st.pyplot(movies['startYear'].hist(bins=12))