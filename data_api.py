import pandas

data_folder = './data/'

genre_mapping = {
    "Romance": ["Romance"],
    "Comedy": ["Comedy"],
    "Action/Adventure": ["Action", "Adventure", "War", "Western"],
    "Crime/Thriller": ["Crime", "Thriller", "Mystery"],
    "Sci-Fi": ["Sci-Fi"],
    "Fantasy": ["Fantasy"],
    "Family": ["Animation", "Family"],
    "Other": ["Drama"]
}

default_region_list = [
    'Americas',
    'Europe',
    'Asia',
    'Oceania',
    'Africa',
    'Other'
]

default_categories = [
    'Crime/Thriller',
    'Romance',
    'Action/Adventure',
    'Comedy',
    'Family',
    'Sci-Fi',
    'Fantasy',
    'Other'
]

default_votes_classes = {
    "5k": 5000,
    "10k": 10000,
    "25k": 25000,
    "100k": 100000,
    "500k": 500000
}

def load_good_movies():
    return pandas.read_parquet(f'{data_folder}good_movies.parquet')

def get_poster_url(movie_info):
    img_url = ''
    if 'poster_path' in movie_info:
        img_url = f'''https://image.tmdb.org/t/p/w500{movie_info['poster_path']}'''
    return img_url
