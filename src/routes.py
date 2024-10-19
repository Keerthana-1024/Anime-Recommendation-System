from flask import Blueprint, render_template, request
from recommendations import recommend_animes
from data_processing import preprocess_data, get_genres, get_anime_types
import pandas as pd
import os
import pandas as pd
base_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(base_dir, '..', 'data', 'anime.csv')
a_df = pd.read_csv(data_file_path)

# a_df = pd.read_csv("data/anime.csv")
feat_mat, processed_df = preprocess_data(a_df)

index = Blueprint('index', __name__)

@index.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        anime_name = request.form['anime_name']
        n_recs = int(request.form['n_recs'])
        genre = request.form.get('genre')
        anime_type = request.form.getlist('anime_type')
        min_rating = request.form['min_rating']
        min_rating = float(min_rating) if min_rating else None

        recommendations = recommend_animes(feat_mat,anime_name, processed_df, n_recs=n_recs, genre=genre, anime_type=anime_type, min_rating=min_rating)
        gg=get_genres(processed_df)
        return render_template('index.html', recommendations=recommendations.to_dict(orient='records'), genres=gg, types=get_anime_types())
    gg=get_genres(processed_df)
    return render_template('index.html', genres=gg, types=get_anime_types())
