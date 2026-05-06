# Movie Recommender System

A full-stack movie recommendation web application built with Python, Flask, MongoDB, and the TMDB API. Users can browse movies, filter by genre/rating/decade/language, sort results, and get personalized movie recommendations based on content similarity.

## Features

- **Movie Browsing** — Browse a curated movie database with rich metadata (title, genre, rating, year, language, poster)
- **Smart Filtering** — Filter movies by genre, minimum rating, decade (2020s, 2010s, 2000s, etc.), and language
- **Flexible Sorting** — Sort results by rating (high/low), year (new/old), or title (A-Z)
- **Content-Based Recommendations** — Enter a movie title and get similar movie recommendations powered by content similarity algorithms
- **TMDB Integration** — Fetches real movie data including posters, ratings, and metadata from The Movie Database (TMDB) API
- **MongoDB Backend** — Stores and queries movie data using MongoDB for fast, flexible document-based retrieval

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python, Flask |
| **Database** | MongoDB (PyMongo) |
| **Data Source** | TMDB API |
| **Frontend** | HTML, CSS (Jinja2 Templates) |
| **Recommendation Engine** | Content-based filtering (recommender.py) |
| **Environment Management** | python-dotenv |

## Project Structure

```
movie-recommender/
├── app.py                 # Flask application — routes, filtering, sorting logic
├── recommender.py         # Recommendation engine — content-based similarity
├── fetch_tmdb.py          # TMDB API data fetcher — pulls movie metadata
├── upload_data.py         # Data upload script — loads movies into MongoDB
├── check_dp.py            # Database check utility — validates data integrity
├── .env                   # Environment variables (MongoDB URI, TMDB API key)
├── data/                  # Raw movie data files
├── templates/             # HTML templates (Jinja2)
│   └── index.html         # Main UI — browsing, filtering, recommendations
└── README.md
```

## How It Works

### 1. Data Pipeline
- `fetch_tmdb.py` connects to the TMDB API and fetches movie data (title, genre, rating, year, language, poster URL)
- `upload_data.py` loads the fetched data into a MongoDB collection
- `check_dp.py` validates the database contents for data integrity

### 2. Web Application
- `app.py` serves a Flask web application with two main routes:
  - **`/` (Browse)** — Displays all movies with filtering (genre, rating, decade, language) and sorting options. Queries MongoDB with dynamic filter construction using regex matching and range queries
  - **`/recommend` (Recommend)** — Accepts a movie title input and returns similar movies using the recommendation engine

### 3. Recommendation Engine
- `recommender.py` implements content-based filtering to find movies similar to a user's input
- Matches are based on movie attributes (genre, rating, metadata) to surface relevant recommendations

## Setup & Installation

### Prerequisites
- Python 3.8+
- MongoDB (local or MongoDB Atlas)
- TMDB API Key (free at https://www.themoviedb.org/settings/api)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/KarnatiNarmada/movie-recommender.git
   cd movie-recommender
   ```

2. **Install dependencies**
   ```bash
   pip install flask pymongo python-dotenv requests
   ```

3. **Configure environment variables**
   Create a `.env` file with:
   ```
   MONGO_URI=your_mongodb_connection_string
   DB_NAME=your_database_name
   COLLECTION_NAME=your_collection_name
   TMDB_API_KEY=your_tmdb_api_key
   ```

4. **Fetch and upload movie data**
   ```bash
   python fetch_tmdb.py
   python upload_data.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   Navigate to `http://localhost:5000`

## Key Technical Highlights

- **Dynamic MongoDB Queries** — Builds query filters programmatically using `$regex`, `$gte`, `$lte` operators based on user selections
- **Flexible Sort System** — Maps user-friendly sort options (e.g., "Highest Rated") to MongoDB sort fields and directions
- **Decade-Based Filtering** — Converts decade selections (2020s, 2010s, etc.) into year range queries using a mapping dictionary
- **API Integration** — Connects to TMDB REST API for real-time movie data retrieval
- **Environment-Based Configuration** — Uses python-dotenv for secure credential management (MongoDB URI, API keys)
- **Content-Based Recommendation** — Implements similarity-based movie matching without requiring user history data

## Skills Demonstrated

- Full-stack web development (Flask + MongoDB + HTML/CSS)
- REST API integration and data ingestion
- NoSQL database design and querying (MongoDB)
- Content-based recommendation algorithms
- Environment variable management and security best practices
- Data pipeline development (fetch → transform → load → serve)

## Author

**Narmada Karnati**
- GitHub: [KarnatiNarmada](https://github.com/KarnatiNarmada)
- LinkedIn: [narmada-karnati](https://www.linkedin.com/in/narmada-karnati-b7b90a190)
