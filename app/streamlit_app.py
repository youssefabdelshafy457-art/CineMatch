import json
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv
import os

# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
st.write("TMDB Key Loaded:", bool(TMDB_API_KEY))
def get_movie_poster(movie_title):
    if not TMDB_API_KEY:
        return None

    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_title,
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()

        if not data.get("results"):
            return None

        poster_path = data["results"][0].get("poster_path")

        if not poster_path:
            return None

        return f"https://image.tmdb.org/t/p/w500{poster_path}"

    except requests.RequestException:
        return None

MOVIES_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "tmdb_5000_movies.csv"
)

API_URL = "http://127.0.0.1:8000"


# ============================================================
# Load Movie Metadata
# ============================================================

@st.cache_data
def load_movies():

    import pandas as pd

    movies = pd.read_csv(MOVIES_PATH)

    movies["id"] = movies["id"].astype(int)

    movies["year"] = (
        pd.to_datetime(
            movies["release_date"],
            errors="coerce"
        )
        .dt.year
        .fillna(0)
        .astype(int)
    )

    def extract_genres(value):

        try:
            data = json.loads(value)

            return " • ".join(
                item["name"]
                for item in data
            )

        except Exception:
            return ""

    movies["genre_names"] = movies["genres"].fillna(
        "[]"
    ).apply(extract_genres)

    movies["poster_url"] = None
    

    return movies


movies = load_movies()


# ============================================================
# Session State
# ============================================================

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None


# ============================================================
# Custom CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =========================
       Global
       ========================= */

    .stApp {
        background:
            radial-gradient(
                circle at 85% 10%,
                rgba(91, 65, 170, 0.18),
                transparent 28%
            ),
            radial-gradient(
                circle at 10% 30%,
                rgba(32, 45, 80, 0.15),
                transparent 30%
            ),
            #080a0f;
        color: #f5f5f5;
    }

    .block-container {
        max-width: 1350px;
        padding-top: 28px;
        padding-bottom: 60px;
    }

    /* =========================
       Header
       ========================= */

    [data-testid="stHeader"] {
        background: transparent;
    }

    .brand {
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .brand span {
        color: #8b5cf6;
    }

    .tagline {
        color: #8b91a1;
        font-size: 13px;
        margin-top: -8px;
    }

    /* =========================
       Hero
       ========================= */

    .hero {
        padding: 65px 30px 55px 30px;
        margin-top: 25px;
        margin-bottom: 30px;
        border-radius: 24px;

        background:
            linear-gradient(
                90deg,
                rgba(8, 10, 15, 0.98) 0%,
                rgba(8, 10, 15, 0.88) 48%,
                rgba(8, 10, 15, 0.45) 100%
            );

        border: 1px solid rgba(255,255,255,0.06);
        box-shadow:
            0 25px 70px rgba(0,0,0,0.35);
    }

    .hero-title {
        font-size: 52px;
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -2px;
        margin-bottom: 16px;
    }

    .hero-title span {
        color: #8b5cf6;
    }

    .hero-text {
        max-width: 650px;
        color: #a4a9b6;
        font-size: 16px;
        line-height: 1.7;
    }

    /* =========================
       Section Titles
       ========================= */

    .section-title {
        font-size: 24px;
        font-weight: 750;
        margin-top: 35px;
        margin-bottom: 4px;
    }

    .section-subtitle {
        color: #777e8d;
        font-size: 13px;
        margin-bottom: 18px;
    }

    /* =========================
       Search
       ========================= */

    div[data-baseweb="input"] {
        background: #12151d !important;
        border: 1px solid #292e3a !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 1px #8b5cf6 !important;
    }

    input {
        color: #111827  !important;
        caret-color: #111827 !important
    }

        /* Recommendation Number */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 12px !important;
    }

    /* Selected number */
    div[data-baseweb="select"] div[role="button"] {
        color: #111827 !important;
        background-color: #ffffff !important;
    }

    div[data-baseweb="select"] div[role="button"] span {
        color: #111827 !important;
    }
    /* =========================
       Buttons
       ========================= */

    .stButton > button {
        background: #8b5cf6;
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        min-height: 44px;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        background: #7c3aed;
        transform: translateY(-1px);
    }

    /* =========================
       Movie Cards
       ========================= */

    .movie-info {
        padding-top: 9px;
    }

    .movie-title {
        font-size: 16px;
        font-weight: 700;
        color: #f4f4f5;
        line-height: 1.25;
        min-height: 42px;
    }

    .movie-meta {
        color: #858b99;
        font-size: 12px;
        margin-top: 5px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .match {
        display: inline-block;
        margin-top: 8px;
        padding: 4px 8px;
        border-radius: 6px;
        background: rgba(139, 92, 246, 0.13);
        color: #a78bfa;
        font-size: 11px;
        font-weight: 700;
    }

    /* =========================
       Selected Movie
       ========================= */

    .selected-box {
        padding: 24px;
        border-radius: 18px;
        background: #10131a;
        border: 1px solid #222733;
        margin-top: 25px;
        margin-bottom: 25px;
    }

    .selected-label {
        color: #8b5cf6;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .selected-title {
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 7px;
    }

    .selected-meta {
        color: #8f95a3;
        font-size: 13px;
    }

    /* =========================
       Footer
       ========================= */

    .footer {
        text-align: center;
        color: #555b68;
        font-size: 12px;
        padding-top: 50px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Header
# ============================================================

header_col1, header_col2 = st.columns(
    [5, 1],
    vertical_alignment="center"
)

with header_col1:

    st.markdown(
        '<div class="brand">Cine<span>Match</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tagline">'
        'Intelligent Movie Recommendation System'
        '</div>',
        unsafe_allow_html=True
    )



# ============================================================
# Hero
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">
            Find your next<br>
            <span>favorite movie.</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        max-width: 650px;
        color: #a4a9b6;
        font-size: 16px;
        line-height: 1.7;
        margin-top: -20px;
        margin-bottom: 30px;
    ">
        Discover movies that match your taste using
        Natural Language Processing, TF-IDF and
        Cosine Similarity.
    </div>
    """,
    unsafe_allow_html=True
)
# ============================================================
# Search
# ============================================================

st.markdown(
    '<div class="section-title">What do you want to watch?</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Search for a movie and CineMatch will find similar titles.'
    '</div>',
    unsafe_allow_html=True
)


search_col, number_col, button_col = st.columns(
    [5, 1.2, 1.5],
    vertical_alignment="bottom"
)

with search_col:

    movie_title = st.text_input(
        "Movie",
        placeholder="Search movies like Avatar, Inception, Titanic...",
        label_visibility="collapsed"
    )

with number_col:

    top_n = st.selectbox(
        "Number",
        [5, 6, 7, 8, 9, 10],
        index=0,
        label_visibility="collapsed"
    )

with button_col:

    search_button = st.button(
        "Find Movies",
        use_container_width=True
    )


# ============================================================
# Search Action
# ============================================================

if search_button:

    if not movie_title.strip():

        st.warning("Please enter a movie title.")

    else:

        try:

            with st.spinner("Finding your next movies..."):

                response = requests.get(
                    f"{API_URL}/recommend/{movie_title}",
                    params={"top_n": top_n},
                    timeout=10
                )

            if response.status_code == 200:

                data = response.json()

                st.session_state.selected_movie = data["movie"]
                st.session_state.recommendations = (
                    data["recommendations"]
                )

            elif response.status_code == 404:

                st.session_state.selected_movie = None
                st.session_state.recommendations = None

                st.error(
                    f"Movie '{movie_title}' was not found."
                )

            else:

                st.error(
                    "Something went wrong with CineMatch API."
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to CineMatch API. "
                "Make sure FastAPI is running."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The request took too long. Please try again."
            )


# ============================================================
# Results
# ============================================================

if (
    st.session_state.selected_movie
    and st.session_state.recommendations
):

    selected_title = st.session_state.selected_movie

    selected_data = movies[
        movies["title"].str.lower()
        == selected_title.lower()
    ]

    # ========================================================
    # Selected Movie
    # ========================================================

    if not selected_data.empty:

        selected = selected_data.iloc[0]

        st.markdown(
            '<div class="selected-box">',
            unsafe_allow_html=True
        )

        poster_col, details_col = st.columns(
            [1, 4],
            vertical_alignment="center"
        )

        with poster_col:

            poster_url = get_movie_poster(selected["title"])

            if poster_url:

                st.image(
                     poster_url,
                    use_container_width=True
                    )

        with details_col:

            st.markdown(
                '<div class="selected-label">'
                'Selected Movie'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="selected-title">'
                f'{selected["title"]}'
                f'</div>',
                unsafe_allow_html=True
            )

            meta = []

            if selected["year"] > 0:
                meta.append(str(selected["year"]))

            if selected["vote_average"] > 0:
                meta.append(
                    f'★ {selected["vote_average"]:.1f}'
                )

            if selected["genre_names"]:
                meta.append(selected["genre_names"])

            st.markdown(
                f'<div class="selected-meta">'
                f'{"  •  ".join(meta)}'
                f'</div>',
                unsafe_allow_html=True
            )

            if isinstance(
                selected["overview"],
                str
            ):

                st.write(
                    selected["overview"]
                )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    # ========================================================
    # Because You Watched
    # ========================================================

    st.markdown(
        f'<div class="section-title">'
        f'Because You Watched {selected_title}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Recommended using content similarity'
        '</div>',
        unsafe_allow_html=True
    )

    recommendations = st.session_state.recommendations

    # ========================================================
    # Movie Row
    # ========================================================

    columns = st.columns(
        len(recommendations)
    )

    for index, (column, recommendation) in enumerate(
        zip(columns, recommendations),
        start=1
    ):

        movie_id = recommendation["movie_id"]
        score = recommendation["score"] * 100

        movie_data = movies[
            movies["id"] == movie_id
        ]
        poster_url = get_movie_poster(recommendation["title"])

        with column:

            if not movie_data.empty:

                movie = movie_data.iloc[0]
                poster_url = get_movie_poster(movie["title"])
                if poster_url:

                    st.image(
                        poster_url,
                        use_container_width=True
                    )

                else:

                    st.image(
                        "https://via.placeholder.com/500x750?text=No+Poster",
                        use_container_width=True
                    )

                st.markdown(
                    '<div class="movie-info">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="movie-title">'
                    f'{movie["title"]}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                metadata = []

                if movie["year"] > 0:
                    metadata.append(
                        str(movie["year"])
                    )

                if movie["vote_average"] > 0:
                    metadata.append(
                        f'★ {movie["vote_average"]:.1f}'
                    )

                st.markdown(
                    f'<div class="movie-meta">'
                    f'{" • ".join(metadata)}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="match">'
                    f'{score:.1f}% MATCH'
                    f'</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )


# ============================================================
# Empty State
# ============================================================

else:

    st.markdown(
        '<div class="section-title">'
        'Popular Movies'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Try searching for one of these movies'
        '</div>',
        unsafe_allow_html=True
    )

    popular_titles = [
        "Avatar",
        "The Dark Knight",
        "Inception",
        "Titanic",
        "Toy Story",
    ]

    popular_columns = st.columns(5)

    for column, title in zip(
        popular_columns,
        popular_titles
    ):

        movie_data = movies[
            movies["title"].str.lower()
            == title.lower()
        ]

        with column:

            if not movie_data.empty:

                movie = movie_data.iloc[0]

                poster_url = get_movie_poster(movie["title"])

                if poster_url:

                    st.image(
                        poster_url,
                        use_container_width=True
                    )

                else:

                    st.image(
                        "https://via.placeholder.com/500x750?text=No+Poster",
                        use_container_width=True
                    )

                st.caption(
                    movie["title"]
                )


# ============================================================
# Footer
# ============================================================

st.markdown(
    '<div class="footer">'
    'CineMatch · Content-Based Movie Recommendation · '
    'TF-IDF + Cosine Similarity'
    '</div>',
    unsafe_allow_html=True
)

