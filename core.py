import random
import urllib
import requests
import pandas
import os
import json
import functools

data_folder = './data/'

def load_good_movies():
    movies = pandas.read_parquet(f'{data_folder}good_movies.parquet')
    ratings = pandas.read_parquet(f'{data_folder}good_ratings.parquet')
    return movies, ratings

def randomize_sequence(total_movies):
    sequence = list(range(0, total_movies))
    random.shuffle(sequence)
    return sequence

def get_poster_url(movie_info):
    img_url = ''
    if 'poster_path' in movie_info:
        img_url = f'''https://image.tmdb.org/t/p/w500{movie_info['poster_path']}'''
    return img_url

def get_poster_path(tconst, movie_info):
    poster_markdown = ''
    img_url = get_poster_url(movie_info)
    poster_path = img_url
    return poster_path

def get_info_from_api(tconst, tmdb_api_key):
    movie_info = {}
    url_request = f'https://api.themoviedb.org/3/find/{tconst}?api_key={tmdb_api_key}&external_source=imdb_id'
    r = requests.get(url_request)
    if r.ok:
        r_jon = r.json()
        movie_results = r_jon['movie_results']
        if len(movie_results) > 0:
            movie_info = movie_results[0]
    return movie_info

def get_info(tconst, tmdb_api_key):
    return get_info_from_api(tconst, tmdb_api_key)

def get_markdown(random_movie, ratings, tmdb_api_key):

    tconst = random_movie['tconst']

    rating = ratings.loc[ratings['tconst'] == tconst].iloc[0]

    movie_info = get_info(tconst, tmdb_api_key)

    poster_path = get_poster_path(tconst, movie_info)

    imdb_link = f'https://www.imdb.com/title/{tconst}/?'

    markdown = f'''
## {random_movie['primaryTitle']}

**IMDB** / **Rating**: {rating['averageRating']}, **Votes**: {rating['numVotes']}, **View**: [link]({imdb_link}).

**Original Title**: {random_movie['originalTitle']}
**Year**: {random_movie['startYear']}
**Runtime (Minutes)**: {random_movie['runtimeMinutes']}
**Genres**: {random_movie['genres']}

**Overview**

{movie_info['overview']}

![{random_movie['primaryTitle']}]({poster_path})

**Information courtesy of IMDb (https://www.imdb.com) and TMDB (https://www.themoviedb.org). Used with permission.**

'''
    
    return markdown

