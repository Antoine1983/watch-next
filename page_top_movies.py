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

def get_top_movies(from_year, minimum_votes, region_list, max_movies, categories_list):
    display_columns = [
        'primaryTitle',
        'averageRating',
        'numVotesK',
        'startYear',
        'url'
    ]
    filtered_movies = get_filtered_movies(from_year, minimum_votes, region_list, categories_list)
    filtered_movies['url'] = filtered_movies['tconst'].map('https://www.imdb.com/title/{}/?'.format)
    filtered_movies['numVotesK'] = filtered_movies['numVotes'] / 1000
    return filtered_movies[display_columns].sort_values(by='averageRating', ascending=False).head(max_movies)


st.title('Top movies')

with st.sidebar:

    st.header('Filters')

    # Filter on rating
    max_movies = st.number_input(
        "Maximum number of movies", 
        min_value=50, 
        max_value=500, 
        value=100,
        step=50
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
        max_movies,
        categories_list
    )

    # Display total
    total_movies = len(best_movies.index)
    st.write(f'Total movies: {total_movies}')

st.dataframe(
    best_movies, 
    hide_index=True,
    use_container_width=True,
    column_config={
        "primaryTitle": "Titre",
        "averageRating": st.column_config.NumberColumn(
            "Average rating",
            format="%.1f ⭐",
        ),
        "url": st.column_config.LinkColumn("IMDB", display_text='View'),
        "numVotesK": st.column_config.ProgressColumn(
            "Votes",
            min_value=5,
            max_value=500,
            format="%.1fk"
        ),
        "startYear": st.column_config.NumberColumn("Year", format="%d")
    },
    height=total_movies * 40
)

st.caption(f'Top {total_movies} movies ranked by average rating.')

# st.pyplot(movies['startYear'].hist(bins=12))