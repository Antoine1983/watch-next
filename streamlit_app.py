import streamlit as st
import core

tmdb_api_key = st.secrets["TMDB_API_KEY"]

st.set_page_config(page_title='What should I watch?')
                   
st.title('What should I watch?')

@st.cache_data(persist="disk")
def init_data():
    return core.load_good_movies()

movies, ratings = init_data()

@st.cache_data(ttl="1h")
def randomize_sequence():
    return core.randomize_sequence(len(movies.index))

sequence = randomize_sequence()

@st.cache_data
def get_markdown(random_index):
    random_movie = movies.iloc[random_index]
    return core.get_markdown(random_movie, ratings, tmdb_api_key)

if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
    
def choose_next():
    st.session_state.current_index += 1
    if st.session_state.current_index >= len(sequence):
        st.session_state.current_index = 0

random_index = sequence[st.session_state.current_index]

with st.spinner('Wait for it...'):
    markdown = get_markdown(random_index)
    st.write(markdown)

st.write('Random Movie Roulette: randomly choose a good movie to watch !') 

if st.button("Try again ?", type="primary"):
    choose_next()
    st.rerun()

st.caption('Information courtesy of IMDb (https://www.imdb.com) and TMDB (https://www.themoviedb.org). Used with permission.')
