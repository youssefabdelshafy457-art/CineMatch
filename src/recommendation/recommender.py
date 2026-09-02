import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:

    def __init__(self, movies_path: str):

        # Load processed movies
        self.movies = pd.read_csv(movies_path)

        # Make sure combined_features has no missing values
        self.movies["combined_features"] = (
            self.movies["combined_features"]
            .fillna("")
        )

        # TF-IDF
        self.tfidf = TfidfVectorizer(
            stop_words="english"
        )

        self.tfidf_matrix = self.tfidf.fit_transform(
            self.movies["combined_features"]
        )

        # Cosine Similarity
        self.similarity_matrix = cosine_similarity(
            self.tfidf_matrix
        )

        # Create title → index mapping
        self.title_to_index = {
            title.lower(): index
            for index, title in enumerate(self.movies["title"])
        }

    def recommend_movies(self, movie_title: str, top_n: int = 5):

        movie_title = movie_title.lower()

        # Check if movie exists
        if movie_title not in self.title_to_index:
            return []

        movie_index = self.title_to_index[movie_title]

        # Get similarity scores
        similarity_scores = list(
            enumerate(
                self.similarity_matrix[movie_index]
            )
        )

        # Sort by similarity
        similarity_scores = sorted(
            similarity_scores,
            key=lambda x: x[1],
            reverse=True
        )

        # Get recommendations
        recommendations = []

        for index, score in similarity_scores[1:top_n + 1]:

            movie_id = int(self.movies.iloc[index]["movie_id"])

            recommendations.append({
                "movie_id": movie_id,
                "title": self.movies.iloc[index]["title"],
                "score": float(score)
    })

        return recommendations