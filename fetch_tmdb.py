import requests
import time
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db[os.getenv("COLLECTION_NAME")]

def get_genres():
    url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}&language=en-US"
    res = requests.get(url).json()
    return {g["id"]: g["name"] for g in res["genres"]}

def fetch_movies(total_pages=500):
    genre_map = get_genres()
    all_movies = []

    print(f"Fetching movies from TMDB — {total_pages} pages...")

    for page in range(1, total_pages + 1):
        url = f"{BASE_URL}/discover/movie"
        params = {
            "api_key": API_KEY,
            "sort_by": "popularity.desc",
            "page": page,
            "vote_count.gte": 100,
        }

        try:
            res = requests.get(url, params=params).json()
            movies = res.get("results", [])

            for m in movies:
                if not m.get("poster_path"):
                    continue

                genre_ids = m.get("genre_ids", [])
                genres = ", ".join([
                    genre_map.get(g, "")
                    for g in genre_ids
                    if g in genre_map
                ])

                movie = {
                    "title":      m.get("title", ""),
                    "overview":   m.get("overview", ""),
                    "genre":      genres,
                    "rating":     m.get("vote_average", 0),
                    "year":       m.get("release_date", "")[:4] if m.get("release_date") else "",
                    "poster":     IMAGE_BASE + m["poster_path"],
                    "director":   "",
                    "cast":       "",
                    "tmdb_id":    m.get("id"),
                    "popularity": m.get("popularity", 0),
                    "language":   m.get("original_language", "")
                }
                all_movies.append(movie)

            print(f"Page {page}/{total_pages} — Total: {len(all_movies)}")
            time.sleep(0.25)

        except Exception as e:
            print(f"Error on page {page}: {e}")
            time.sleep(2)
            continue

    return all_movies

def upload_to_mongo(movies):
    print(f"\nUploading {len(movies)} movies to MongoDB...")
    collection.drop()

    batch_size = 500
    for i in range(0, len(movies), batch_size):
        batch = movies[i:i + batch_size]
        collection.insert_many(batch)
        print(f"Uploaded {min(i + batch_size, len(movies))}/{len(movies)}")

    total = collection.count_documents({})
    print(f"\n✅ Done! {total} movies in MongoDB")

if __name__ == "__main__":
    movies = fetch_movies(total_pages=500)
    upload_to_mongo(movies)