import streamlit as st
import data_api


@st.cache_data
def load_good_movies():
    return data_api.load_good_movies()

def get_filtered_movies(from_year, minimum_votes, region_list, categories_list):
    movies = load_good_movies()
    movies['genres_list'] = movies['genres'].str.split(',')
    c1 = movies['startYear'] >= from_year
    c2 = movies['numVotes'] >= minimum_votes
    c3 = movies['country_region'].isin(region_list)
    check_list = sum([data_api.genre_mapping[category] for category in categories_list], [])
    c5 = movies['genres_list'].apply(lambda x: any(item in check_list for item in x))
    return movies.loc[c1 & c2 & c3 & c5]

@st.cache_data
def get_top_movies(from_year, minimum_votes, region_list, categories_list):
    filtered_movies = get_filtered_movies(from_year, minimum_votes, region_list, categories_list)
    best_movies = filtered_movies.sort_values(by='averageRating', ascending=False)
    best_movies['rank'] = range(1, len(best_movies) + 1)
    return best_movies


with st.sidebar:

    st.header('Filters')

    # Filter on rating
    max_movies = st.number_input(
        "Movies per page",
        min_value=10,
        max_value=250,
        value=25,
        step=5
    )

    # Filter on start year
    from_year = st.number_input(
        "From year",
        min_value=1970,
        value=1970,
        step=10
    )

    # Filter on regions
    region_list = st.multiselect(
        'Regions',
        data_api.default_region_list,
        default=data_api.default_region_list
    )

    # Filter on categories
    categories_list = st.multiselect(
        'Categories',
        data_api.default_categories,
        default=data_api.default_categories
    )

    # Filter on number of votes
    minimum_votes_class = st.select_slider(
        "Minimum number of votes",
        options=data_api.default_votes_classes,
        value='500k'
    )
    minimum_votes = data_api.default_votes_classes[minimum_votes_class]

    # Get filtered movies
    best_movies = get_top_movies(
        from_year,
        minimum_votes,
        region_list,
        categories_list
    )

    # Display total
    total_movies = len(best_movies.index)
    st.write(f'Total movies: {total_movies}')


st.title(f'Top movies by rating', anchor='top-of-page')

# Pagination
current_page = st.selectbox('Page', options=range(1, int(total_movies / max_movies + 2)))
from_item = max_movies * (current_page - 1)
to_item = max_movies * current_page

# Show the movies
for index, movie in best_movies[from_item:to_item].iterrows():

    st.divider()

    tconst = movie['tconst']
    imdb_link = f'https://www.imdb.com/title/{tconst}/?'

    markdown = f'''
    **IMDB** / **Rating**: {movie['averageRating']} ⭐,
    **Votes**: {movie['numVotes'] / 1000:.1f}k,
    **View**: [link]({imdb_link}).

    **Region**: {movie['country_region']},
    **Country**: {movie['country_name']},
    **Year**: {movie['startYear']},
    **Runtime (Minutes)**: {movie['runtimeMinutes']},
    **Genres**: {movie['genres']}

    **Original Title**: {movie['originalTitle']}
    '''


    col1, col2 = st.columns([3, 1])

    # Show details
    with col1:
        st.subheader(f'''{movie['rank']} - {movie['primaryTitle']}''')
        st.markdown(markdown)
        with st.expander("Overview"):
            st.write(movie['overview'])

    # Show poster
    with col2:
        poster_caption = f'''{movie['primaryTitle']} ({movie['startYear']})'''
        poster_url = data_api.get_poster_url(movie)
        st.markdown(f"[![{poster_caption}]({poster_url})]({imdb_link})")

st.divider()

st.write('<a href="#top-of-page">Scroll up</a>', unsafe_allow_html = True)
