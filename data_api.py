import random
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
