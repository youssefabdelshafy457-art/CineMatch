from fastapi import FastAPI, HTTPException
from pathlib import Path

from src.recommendation.recommender import MovieRecommender


app = FastAPI(
    title="CineMatch API",
    description="Intelligent Movie Recommendation System",
    version="1.0.0"
)
# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize recommendation engine
recommender = MovieRecommender(
    str(BASE_DIR / "data" / "processed" / "movies_processed.csv")
)


@app.get("/")
def root():
    return {
        "message": "Welcome to CineMatch API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/recommend/{movie_title}")
def recommend(movie_title: str, top_n: int = 5):

    recommendations = recommender.recommend_movies(
        movie_title,
        top_n
    )

    if not recommendations:
        raise HTTPException(
            status_code=404,
            detail=f"Movie '{movie_title}' not found"
        )

    return {
        "movie": movie_title,
        "recommendations": recommendations
    }