import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load ratings
def load_data():
    columns_names = ['user_id','item_id','rating','timestamp']
    ratings = pd.read_csv("u.data", sep='\t', names=columns_names)

    # Load movie titles
    movie_titles = pd.read_csv("u.item", sep='|', encoding='latin-1', usecols=[0, 1], names=['item_id', 'movie_title'])
    
    # Merge datasets
    data = pd.merge(ratings, movie_titles, on='item_id')
    return data

# Create pivot table and similarity matrix
def prepare_similarity_matrix(data):
    movie_matrix = data.pivot_table(index='user_id', columns='movie_title', values='rating')
    movie_matrix.fillna(0, inplace=True)

    # Transpose for item-item similarity
    movie_similarity = cosine_similarity(movie_matrix.T)
    similarity_df = pd.DataFrame(movie_similarity, index=movie_matrix.columns, columns=movie_matrix.columns)
    return similarity_df

# Get recommendations
def get_recommendations(movie_title, similarity_df, n=5):
    if movie_title not in similarity_df.columns:
        return ["Movie not found in database."]
    
    similar_scores = similarity_df[movie_title].sort_values(ascending=False)
    top_movies = list(similar_scores.iloc[1:n+1].index)  # skip the first (itself)
    return top_movies

# For testing
if __name__ == "__main__":
    data = load_data()
    similarity_df = prepare_similarity_matrix(data)
    movie = "Toy Story (1995)"
    print(f"\nTop 5 Recommendations for '{movie}':")
    print(get_recommendations(movie, similarity_df))

