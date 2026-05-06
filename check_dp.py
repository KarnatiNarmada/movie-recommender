from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db[os.getenv("COLLECTION_NAME")]

total = collection.count_documents({})
print(f"Total movies in MongoDB: {total}")

# Show a sample movie
sample = collection.find_one({}, {"_id": 0})
print(f"\nSample movie: {sample}")