import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import re

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db[os.getenv("COLLECTION_NAME")]

df = pd.read_csv("data/imdb_top_1000.csv")
df = df.fillna("")

# Fix poster URLs — replace small size with large size
def fix_poster_url(url):
    if not url:
        return url
    # Remove size constraints like _UX67_, _UY98_, _CR0,0,67,98_ etc
    url = re.sub(r'_UX\d+_', '_UX800_', url)
    url = re.sub(r'_UY\d+_', '_UY1200_', url)
    url = re.sub(r'_CR[\d,]+_', '', url)
    url = re.sub(r'_V1_.*?(@)', r'_V1_\1', url)
    return url

df["Poster_Link"] = df["Poster_Link"].apply(fix_poster_url)

df["cast"] = (df["Star1"] + " " + df["Star2"] + " " +
              df["Star3"] + " " + df["Star4"])

df = df[["Series_Title", "Genre", "Overview", "Director",
         "cast", "IMDB_Rating", "Poster_Link", "Released_Year"]]

df.columns = ["title", "genre", "overview", "director",
              "cast", "rating", "poster", "year"]

movies = df.to_dict(orient="records")

collection.drop()
collection.insert_many(movies)

print(f" Uploaded {len(movies)} movies with HD posters!")