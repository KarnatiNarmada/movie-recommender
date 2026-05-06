from flask import Flask, render_template, request
from recommender import get_recommendations
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db[os.getenv("COLLECTION_NAME")]

@app.route("/", methods=["GET"])
def index():
    genre  = request.args.get("genre",  None)
    rating = request.args.get("rating", None)
    decade = request.args.get("decade", None)
    sort   = request.args.get("sort",   "title_asc")
    language = request.args.get("language", None)

    query = {}

    if genre:
        query["genre"] = {"$regex": genre, "$options": "i"}
    
    if language:
        query["language"] = language

    if rating:
        query["rating"] = {"$gte": float(rating)}

    if decade:
        decade_map = {
            "2020s": ("2020", "2029"),
            "2010s": ("2010", "2019"),
            "2000s": ("2000", "2009"),
            "1990s": ("1990", "1999"),
            "1980s": ("1980", "1989"),
            "Older": ("1900", "1979"),
        }
        if decade in decade_map:
            start, end = decade_map[decade]
            query["year"] = {"$gte": start, "$lte": end}

    sort_map = {
        "rating_desc": ("rating", -1),
        "rating_asc":  ("rating",  1),
        "year_desc":   ("year",   -1),
        "year_asc":    ("year",    1),
        "title_asc":   ("title",   1),
    }
    sort_field, sort_dir = sort_map.get(sort, ("rating", -1))

    total  = collection.count_documents(query)
    movies = list(
        collection.find(query, {"_id": 0})
                  .sort(sort_field, sort_dir)
                  .limit(40)
    )

    return render_template("index.html",
                           movies=movies,
                           searched=None,
                           recommendations=None,
                           query=None,
                           error=None,
                           active_genre=genre,
                           active_rating=rating,
                           active_decade=decade,
                           active_sort=sort,
                           active_language=language,
                           total=total)

@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    query = request.form.get("movie_title", "").strip()

    if not query:
        return render_template("index.html",
                               movies=[],
                               searched=None,
                               recommendations=None,
                               query=None,
                               error="Please enter a movie name.",
                               active_genre=None,
                               active_rating=None,
                               active_decade=None,
                               active_sort=None,
                               active_language=language,
                               total=0)

    searched_movie, result = get_recommendations(query)

    if searched_movie is None:
        return render_template("index.html",
                               movies=[],
                               searched=None,
                               recommendations=None,
                               query=query,
                               error=result,
                               active_genre=None,
                               active_rating=None,
                               active_decade=None,
                               active_sort=None,
                               active_language=language,
                               total=0)

    return render_template("index.html",
                           movies=[],
                           searched=searched_movie,
                           recommendations=result,
                           query=query,
                           error=None,
                           active_genre=None,
                           active_rating=None,
                           active_decade=None,
                           active_sort=None,
                           active_language=language,
                           total=0)


if __name__ == "__main__":
    app.run(debug=True)