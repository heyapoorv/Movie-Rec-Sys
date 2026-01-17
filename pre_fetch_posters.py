import joblib
import requests
from tqdm import tqdm
import streamlit as st

movies = joblib.load("new.pkl")
  # your original movie dataset with 'id'
TMDB_JWT = st.secrets["TMDB_JWT"]  # put your TMDB v4 token here

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {"Authorization": f"Bearer {TMDB_JWT}"}
    params = {"language": "en-US"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except:
        return None
    return None

# Pre-fetch posters
movies['poster_url'] = [fetch_poster(mid) or "https://via.placeholder.com/500x750?text=No+Poster" for mid in tqdm(movies['id'])]

# Save updated dataset
joblib.dump(movies, "movies_with_posters.pkl")
print("Saved movies_with_posters.pkl with poster URLs")
