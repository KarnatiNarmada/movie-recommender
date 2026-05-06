import pandas as pd
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db[os.getenv("COLLECTION_NAME")]

def load_movies():
    movies = list(collection.find({}, {"_id": 0}))
    df = pd.DataFrame(movies)
    return df

def build_features(df):
    df["features"] = (
        df["genre"].fillna("") + " " +
        df["genre"].fillna("") + " " +
        df["overview"].fillna("")
    )
    return df

def get_recommendations(movie_title, num_recommendations=5):
    df = load_movies()

    if df.empty:
        return None, "No movies found in database."

    df = build_features(df)

    movie_title_lower = movie_title.lower()
    df["title_lower"] = df["title"].str.lower()

    if movie_title_lower not in df["title_lower"].values:
        return None, f"Movie '{movie_title}' not found. Try another title."

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["features"])

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    idx = df[df["title_lower"] == movie_title_lower].index[0]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations + 1]

    movie_indices = [i[0] for i in sim_scores]

    recommendations = df.iloc[movie_indices][
        ["title", "genre", "director", "cast",
         "rating", "poster", "year"]
    ].to_dict(orient="records")

    searched_movie = df[df["title_lower"] == movie_title_lower][
        ["title", "genre", "director", "cast",
         "rating", "poster", "year"]
    ].to_dict(orient="records")[0]

    return searched_movie, recommendations