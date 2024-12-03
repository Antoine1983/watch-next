import random
import requests
import pandas

data_folder = './data/'

def load_good_movies():
    return pandas.read_parquet(f'{data_folder}good_movies.parquet')

def randomize_sequence(total_movies):
    sequence = list(range(0, total_movies))
    random.shuffle(sequence)
    return sequence

def get_poster_url(movie_info):
    img_url = ''
    if 'poster_path' in movie_info:
        img_url = f'''https://image.tmdb.org/t/p/w500{movie_info['poster_path']}'''
    return img_url

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



