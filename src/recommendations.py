from sklearn.metrics.pairwise import cosine_similarity

def recommend_animes(feat_mat,anime_name,data, n_recs=10, genre=None, anime_type=None, min_rating=None):
    target_anime = data[data['name'].str.contains(anime_name, case=False, na=False)]
    if target_anime.empty:
        return []

    target_idx = target_anime.index[0]
    target_feat = feat_mat.iloc[target_idx].values.reshape(1, -1)
    cos_sim = cosine_similarity(feat_mat, target_feat)
    sim_indices = cos_sim.flatten().argsort()[::-1][1:]  # Get all except the target

    rec_animes = data.iloc[sim_indices][['anime_id', 'name', 'genre', 'rating', 'type', 'members']].reset_index(drop=True)

    # Store similarity scores in a new column
    rec_animes['similarity_score'] = cos_sim.flatten()[sim_indices]*100

    if genre:
        genre_set = set(genre.split(','))
        rec_animes = rec_animes[rec_animes['genre'].apply(lambda x: any(g in x for g in genre_set))]

    if anime_type:
        rec_animes = rec_animes[rec_animes['type'].isin(anime_type)]

    if min_rating is not None:
        rec_animes = rec_animes[rec_animes['rating'] >= min_rating]
    
    rec_animes = rec_animes.sort_values(by='members', ascending=False)

    return rec_animes.head(n_recs)
