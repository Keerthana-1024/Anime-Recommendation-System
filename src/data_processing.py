import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def preprocess_data(df):
    df['genre'] = df['genre'].fillna('')
    all_genres = set()
    for genre_list in df['genre'].apply(lambda x: x.split(',') if isinstance(x, str) else []):
        all_genres.update(genre_list)
    
    for genre in all_genres:
        df[genre] = df['genre'].apply(lambda x: 1 if genre in x else 0)
    
    encoder_type = OneHotEncoder()
    types_encoded = encoder_type.fit_transform(df[['type']].fillna('nan')).toarray()
    
    scaler = StandardScaler()
    df[['rating_scaled', 'members_scaled']] = scaler.fit_transform(df[['rating', 'members']].fillna(0))
    
    genre_cols = list(all_genres)
    feature_matrix = pd.concat([df[genre_cols], pd.DataFrame(types_encoded), df[['rating_scaled', 'members_scaled']]], axis=1)
    
    return feature_matrix, df

def get_genres(processed_df):
    return list(processed_df['genre'].str.split(',').explode().unique())

def get_anime_types():
    return ['TV', 'Movie', 'OVA', 'Special', 'Music', 'ONA', 'nan']
