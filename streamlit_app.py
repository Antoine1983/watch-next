import streamlit as st
import core

tmdb_api_key = st.secrets["TMDB_API_KEY"]

st.set_page_config(page_title='What should I watch?')
                   
st.title('What should I watch?')

@st.cache_data
def init_data():
    return core.load_good_movies()

movies, ratings, sequence = init_data()

if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
    
def choose_next():
    st.session_state.current_index += 1
    if st.session_state.current_index >= len(sequence):
        st.session_state.current_index = 0

random_index = sequence[st.session_state.current_index]
random_movie = movies.iloc[random_index]

with st.spinner('Wait for it...'):
    markdown = core.get_markdown(random_movie, ratings, tmdb_api_key)
    st.write(markdown)

st.write('Random Movie Roulette: randomly choose a good movie to watch !') 

if st.button("Try again ?"):
    choose_next()
    st.rerun()
