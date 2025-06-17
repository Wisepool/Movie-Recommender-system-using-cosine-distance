import streamlit as st
import pickle as pk
import pandas as pd
import requests

API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except Exception as e:
        print(f"Error fetching poster for ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movie_list:
        try:
            movie_id = movies.iloc[i[0]].id 
            recommended_movies.append(movies.iloc[i[0]]['title'])
            recommended_movies_poster.append(fetch_poster(movie_id))
        except Exception as e:
            print(f"Error in recommendation: {e}")
            recommended_movies.append("Unknown")
            recommended_movies_poster.append("https://via.placeholder.com/500x750?text=No+Image")

    return recommended_movies, recommended_movies_poster



st.header('Movie Recommender System')

movies_dict = pk.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pk.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)


if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
