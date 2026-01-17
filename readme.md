🎬 Movie Recommendation System

A content-based movie recommendation system built using TF-IDF vectorization and cosine similarity, deployed as an interactive Streamlit web application.
Movie posters are fetched dynamically using the TMDB API.

🔍 Overview

This project recommends movies similar to a selected movie based on textual metadata such as genres, overview, keywords, and cast.
It does not rely on user ratings or popularity for now, ensuring pure content-based recommendations.

🧠 Recommendation Logic

Combine relevant movie metadata into a single text feature

Apply TF-IDF Vectorization

Compute Cosine Similarity between movies

Recommend top-N most similar movies

Fetch posters using TMDB Movie ID

🛠 Tech Stack

Python

Pandas

Scikit-learn

TF-IDF Vectorizer

Streamlit

TMDB API

Joblib


✨ Features

Content-based recommendations

Fast similarity search using cached TF-IDF

Poster fetching via TMDB API

Graceful handling of missing posters

Clean and responsive UI


⚠️ Limitations

No collaborative filtering

Some posters may not load due to TMDB rate limits

Popularity and vote averages not yet used

🚀 Future Enhancements

Hybrid recommender (content + popularity)

Use vote_average and vote_count

Search autocomplete

User feedback loop

Performance optimizations

👨‍💻 Author

Apoorv Deshmukh
