# 🎬 CineMatch — Intelligent Movie Recommendation System

CineMatch is an intelligent **Content-Based Movie Recommendation System** that recommends movies based on their similarity to a selected movie.

The system uses **Natural Language Processing (NLP)** techniques to understand movie characteristics and generate personalized recommendations using **TF-IDF Vectorization** and **Cosine Similarity**.

---

## 🚀 Project Overview

CineMatch analyzes information about movies such as:

* Movie overview
* Genres
* Keywords
* Cast
* Director

These features are combined into a single textual representation and processed using NLP techniques.

The system then calculates the similarity between movies and recommends the most relevant titles based on the selected movie.

---

## 🧠 How It Works

The recommendation pipeline follows these steps:

```text
Movie Dataset
      ↓
Data Preprocessing
      ↓
Feature Combination
      ↓
TF-IDF Vectorization
      ↓
Cosine Similarity
      ↓
Movie Similarity Scores
      ↓
Top-N Recommendations
```

### 1. Data Preparation

The project uses the **TMDB 5000 Movie Dataset**.

The dataset is cleaned and processed to prepare the required movie information.

### 2. Feature Engineering

Relevant movie attributes are combined into a single feature called:

```text
combined_features
```

This feature contains information such as:

```text
Overview + Genres + Keywords + Cast + Director
```

### 3. TF-IDF

**Term Frequency–Inverse Document Frequency (TF-IDF)** is used to convert the textual movie information into numerical vectors.

This allows the system to represent each movie based on the importance of the words contained in its features.

### 4. Cosine Similarity

The system calculates **Cosine Similarity** between movie vectors.

Movies with higher similarity scores are considered more relevant to the selected movie.

### 5. Recommendations

The system sorts the similarity scores and returns the **Top-N most similar movies**.

---

## 🏗️ System Architecture

CineMatch consists of three main components:

### Backend — FastAPI

The backend exposes a REST API responsible for:

* Receiving the selected movie
* Running the recommendation algorithm
* Returning movie recommendations
* Returning similarity scores

Example endpoint:

```text
GET /recommend/{movie_title}
```

Example:

```text
/recommend/Avatar?top_n=5
```

### Recommendation Engine

The recommendation engine is implemented using:

* Python
* Pandas
* Scikit-learn
* TF-IDF
* Cosine Similarity

### Frontend — Streamlit

The frontend provides a modern and interactive interface where users can:

1. Search for a movie
2. Select the number of recommendations
3. Get similar movies
4. View movie posters
5. View similarity scores

Movie posters are retrieved dynamically using the **TMDB API**.

---

## 🛠️ Technologies Used

| Technology       | Purpose                             |
| ---------------- | ----------------------------------- |
| Python           | Core programming language           |
| Pandas           | Data manipulation and preprocessing |
| Scikit-learn     | TF-IDF and Cosine Similarity        |
| NLP              | Text-based movie representation     |
| FastAPI          | Backend REST API                    |
| Streamlit        | Interactive web interface           |
| TMDB API         | Movie poster retrieval              |
| Jupyter Notebook | Data analysis and experimentation   |
| Git & GitHub     | Version control                     |

---

## 📂 Project Structure

```text
CineMatch/
│
├── api/
│   └── main.py
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── raw/
│   │   ├── tmdb_5000_movies.csv
│   │   └── tmdb_5000_credits.csv
│   │
│   └── processed/
│       └── movies_processed.csv
│
├── notebooks/
│   ├── 01_eda.ipynb
│   └── 02_recommendation.ipynb
│
├── src/
│   ├── recommendation/
│   │   └── recommender.py
│   │
│   └── utils/
│       └── posters.py
│
├── .gitignore
└── README.md
```

---

## ✨ Key Features

* 🎬 Content-Based Movie Recommendation
* 🧠 NLP-powered feature extraction
* 📊 TF-IDF Vectorization
* 🔍 Cosine Similarity
* ⚡ FastAPI REST API
* 🎨 Interactive Streamlit UI
* 🖼️ Dynamic movie posters
* 🔢 Configurable number of recommendations
* 📈 Similarity scores for recommendations
* 🧹 Data preprocessing and feature engineering

---

## 🎯 Example

If the user searches for:

```text
Avatar
```

CineMatch analyzes the movie's characteristics and returns movies that are most similar based on their content.

The recommendations are ranked according to their cosine similarity scores.

---

## 👨‍💻 My Role

I designed and developed the CineMatch recommendation pipeline from data preparation to the interactive application.

My work included:

* Preparing and preprocessing the movie dataset
* Performing exploratory data analysis
* Designing the movie feature engineering pipeline
* Combining multiple movie attributes into a unified feature representation
* Implementing TF-IDF vectorization
* Implementing Cosine Similarity
* Building the content-based recommendation engine
* Developing the FastAPI backend
* Developing the Streamlit frontend
* Integrating the TMDB API for movie posters
* Connecting the frontend with the recommendation API
* Testing and debugging the complete application
* Structuring the project for version control using Git and GitHub

---

## 🔮 Future Improvements

The current version uses a **Content-Based Recommendation** approach.

Future versions could extend CineMatch into a **Hybrid Recommendation System** by combining content-based recommendations with user behavior and ratings.

Possible improvements include:

* User rating system
* Collaborative Filtering
* Hybrid Recommendation
* Personalized user profiles
* Advanced NLP embeddings
* Semantic Search
* Movie details and trailers
* Recommendation explanations
* Deployment to a cloud platform

---

## 📌 Project Status

**Current Version:** Content-Based Movie Recommendation System

**Status:** Completed

The system successfully combines an NLP-based recommendation engine with a FastAPI backend and an interactive Streamlit frontend.

---

## 📜 License

This project was developed for educational and portfolio purposes.
