import streamlit as st
import data_api
import random

@st.cache_data
def init_data():
    return data_api.load_good_movies()

@st.cache_data(ttl="1h")
def randomize_sequence(total_movies):
    sequence = list(range(0, total_movies))
    random.shuffle(sequence)
    return sequence

st.set_page_config(
    page_title='What should I watch?',
    initial_sidebar_state='auto'
)

# Init data
movies = init_data()

st.title('What should I watch?')

with st.sidebar:

    st.header('Filters')

    # Filter on rating
    minimum_rating = st.number_input(
        "Minimum rating", 
        min_value=7.0, 
        max_value=10.0, 
        value=7.0,
        step=0.5
    )

    # Filter on start year
    from_year = st.number_input(
        "From year",
        min_value=1970,
        value=1970,
        step=10
    )

    # Filter on regions
    default_region_list = ['Americas', 'Europe', 'Asia', 'Oceania', 'Africa']
    region_list = st.multiselect(
        'Regions', 
        default_region_list, 
        default=default_region_list
    )

    # Filter on number of votes
    votes_classes = {
        "10k": 10000,
        "25k": 25000,
        "100k": 100000,
        "500k": 500000
    }
    minimum_votes_class = st.select_slider(
        "Minimum number of votes",
        options=votes_classes,
    )
    minimum_votes = votes_classes[minimum_votes_class]

    # Apply filters
    c1 = movies['startYear'] >= from_year
    c2 = movies['numVotes'] >= minimum_votes
    c3 = movies['country_region'].isin(region_list)
    c4 = movies['averageRating'] >= minimum_rating
    filtered_movies = movies.loc[c1 & c2 & c3 & c4]

    # Display total
    total_movies = len(filtered_movies.index)
    st.write(f'Total movies: {total_movies}')


sequence = randomize_sequence(total_movies)


if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

def choose_next():
    st.session_state.current_index += 1
    if st.session_state.current_index >= len(sequence):
        st.session_state.current_index = 0

if total_movies > 0:

    # Get movie
    random_index = sequence[st.session_state.current_index]
    random_movie = filtered_movies.iloc[random_index]
    tconst = random_movie['tconst']

    with st.spinner('Wait for it...'):

        imdb_link = f'https://www.imdb.com/title/{tconst}/?'

        markdown = f'''
        **IMDB** / **Rating**: {random_movie['averageRating']}, **Votes**: {random_movie['numVotes'] / 1000:.1f}k, **View**: [link]({imdb_link}).

        **Region**: {random_movie['country_region']},
        **Country**: {random_movie['country_name']},
        **Year**: {random_movie['startYear']},
        **Runtime (Minutes)**: {random_movie['runtimeMinutes']},
        **Genres**: {random_movie['genres']}

        **Original Title**: {random_movie['originalTitle']}
        '''

        col1, col2 = st.columns(2)

        # Show details
        with col1:
            st.header(random_movie['primaryTitle'])
            st.markdown(markdown)
            st.subheader('Overview')
            st.write(random_movie['overview'])

        # Show poster
        with col2:
            poster_caption = f'''{random_movie['primaryTitle']} ({random_movie['startYear']})'''
            poster_url = data_api.get_poster_url(random_movie)
            st.markdown(f"[![{poster_caption}]({poster_url})]({imdb_link})")

    st.write('Random Movie Roulette: randomly choose a good movie to watch !') 

    st.button("Try again ?", type="primary", on_click=choose_next)

else:
    st.write('Please review your filtration criteria.')

st.caption('Information courtesy of IMDb (https://www.imdb.com) and TMDB (https://www.themoviedb.org).')

st.caption('Used with permission for non-commercial usage.')
