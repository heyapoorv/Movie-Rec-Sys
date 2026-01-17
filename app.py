import streamlit as st
import pandas as pd
import joblib
from sklearn.metrics.pairwise import linear_kernel
from concurrent.futures import ThreadPoolExecutor
import requests
import time

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="🎬 Movie Recommendation System",
    layout="wide"
)

st.title("🎬 Movie Recommendation System")
st.write("Content-based recommender using TF-IDF (TMDB dataset)")

# -------------------------------
# LOAD MODELS & DATA
# -------------------------------
@st.cache_resource
def load_models():
    movies = joblib.load("new.pkl")          # must contain: title/original_title, id, tags
    tfidf_matrix = joblib.load("tfidf_matrix.pkl")
    indices = joblib.load("indices.pkl")     # title -> index mapping
    return movies, tfidf_matrix, indices

movies, tfidf_matrix, indices = load_models()
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# -------------------------------
# TMDB POSTER FETCH
# -------------------------------
TMDB_JWT = st.secrets["TMDB_JWT"]  # v4 access token

def fetch_poster(movie_id, retries=3, delay=1):
    """Fetch poster URL with retry; return placeholder on failure"""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {"Authorization": f"Bearer {TMDB_JWT}"}
    params = {"language": "en-US"}

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
            return "https://via.placeholder.com/500x750?text=No+Poster"
        except requests.exceptions.RequestException:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return "https://via.placeholder.com/500x750?text=No+Poster"

def fetch_posters_parallel(movie_ids, max_workers=5):
    """Fetch multiple posters concurrently"""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        poster_urls = list(executor.map(fetch_poster, movie_ids))
    return poster_urls

# -------------------------------
# RECOMMEND FUNCTION
# -------------------------------
def recommend(title, top_n=5):
    idx = indices[title]
    if isinstance(idx, pd.Series):
        idx = idx.iloc[0]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    movie_indices = [i[0] for i in sim_scores]

    return movies.iloc[movie_indices][['original_title', 'id']]

# -------------------------------
# STREAMLIT UI
# -------------------------------
movie_name = st.selectbox("Select a movie", movies['original_title'].values)
top_n = st.slider("Number of recommendations", 5, 10, 20)

if st.button("Recommend 🎥"):
    with st.spinner("Fetching recommendations... 🍿"):
        recommendations = recommend(movie_name, top_n)
        movie_ids = [row.id for row in recommendations.itertuples()]
        poster_urls = fetch_posters_parallel(movie_ids, max_workers=5)

    st.success("Here are your recommendations! 🎉")
    st.subheader("Recommended Movies")

    cols = st.columns(5)
    for i, (row, poster_url) in enumerate(zip(recommendations.itertuples(), poster_urls)):
        with cols[i % 5]:
            st.image(poster_url, width='stretch')
            st.caption(row.original_title)
