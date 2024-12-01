import streamlit as st
import data_api

tmdb_api_key = st.secrets["TMDB_API_KEY"]

st.set_page_config(page_title='What should I watch?')
                   
st.title('What should I watch?')

@st.cache_data
def init_data():
    return data_api.load_good_movies()

movies, ratings = init_data()

@st.cache_data(ttl="1h")
def randomize_sequence():
    return data_api.randomize_sequence(len(movies.index))

sequence = randomize_sequence()

@st.cache_data
def get_info_from_api(tconst):
    return data_api.get_info_from_api(tconst, tmdb_api_key)

if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
    
def choose_next():
    st.session_state.current_index += 1
    if st.session_state.current_index >= len(sequence):
        st.session_state.current_index = 0

# Get movie
random_index = sequence[st.session_state.current_index]
random_movie = movies.iloc[random_index]
tconst = random_movie['tconst']

# Get info
movie_info = get_info_from_api(tconst)
rating = ratings.loc[ratings['tconst'] == tconst].iloc[0]

imdb_link = f'https://www.imdb.com/title/{tconst}/?'

markdown = f'''
**IMDB** / **Rating**: {rating['averageRating']}, **Votes**: {rating['numVotes'] / 1000:.1f}k, **View**: [link]({imdb_link}).

**Original Title**: {random_movie['originalTitle']}
**Year**: {random_movie['startYear']}
**Runtime (Minutes)**: {random_movie['runtimeMinutes']}
**Genres**: {random_movie['genres']}
'''

col1, col2 = st.columns(2)

# Show details
with col1:
    st.header(random_movie['primaryTitle'])
    st.markdown(markdown)
    st.subheader('Overview')
    st.write(movie_info['overview'])

# Show poster
with col2:
    poster_caption = f'''{random_movie['primaryTitle']} ({random_movie['startYear']})'''
    poster_url = data_api.get_poster_url(movie_info)
    st.markdown(f"[![{poster_caption}]({poster_url})]({imdb_link})")

st.write('Random Movie Roulette: randomly choose a good movie to watch !') 

if st.button("Try again ?", type="primary"):
    choose_next()
    st.rerun()

st.caption('Information courtesy of IMDb (https://www.imdb.com) and TMDB (https://www.themoviedb.org).')

st.caption('Used with permission for non-commercial usage.')
