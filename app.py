import streamlit as st
from recommendation import load_data, prepare_similarity_matrix, get_recommendations

# Load and prepare data
@st.cache_data
def setup():
    data = load_data()
    similarity_df = prepare_similarity_matrix(data)
    all_movies = sorted(data['movie_title'].unique())
    return data, similarity_df, all_movies

data, similarity_df, movie_list = setup()

# Page configuration
st.set_page_config(page_title="Movie Recommendation System", layout="centered")

# Title and instructions
st.title("🎬 Movie Recommendation System")
st.markdown("Get top movie recommendations based on your favorite movie!")

# Movie selection
selected_movie = st.selectbox("Choose a movie you like:", movie_list)

# Button to get recommendations
if st.button("Get Recommendations"):
    with st.spinner("Finding similar movies..."):
        recommendations = get_recommendations(selected_movie, similarity_df)
    
    st.subheader("🎯 Recommended Movies:")
    for idx, movie in enumerate(recommendations, start=1):
        st.write(f"{idx}. {movie}")
