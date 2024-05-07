import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
                return full_path
            else:
                return None
        else:
            return None
    except Exception as e:
        print("Error fetching poster:", e)
        return None

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
        recommend_movie = []
        recommend_poster = []
        for i in distance[1:6]:
            movies_id = movies.iloc[i[0]].id
            recommend_movie.append(movies.iloc[i[0]].title)
            poster = fetch_poster(movies_id)
            if poster:
                recommend_poster.append(poster)
            else:
                # Handle case where poster is not available
                recommend_poster.append("Poster not available")
        return recommend_movie, recommend_poster
    except IndexError:
        print("Movie not found in dataset")
        return [], []

movies = pickle.load(open("movies_list", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_lists = movies['title'].values

st.header("Movie Recommender System")

import streamlit.components.v1 as components

imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")


imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
   
    ]


imageCarouselComponent(imageUrls=imageUrls, height=200)
selectvalue=st.selectbox("Select movie from dropdown", movies_lists)

if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selectvalue)
    col1, col2, col3, col4, col5 = st.columns(5)
    for i in range(5):
        with globals()[f"col{i+1}"]:
            if i < len(movie_name):
                st.text(movie_name[i])
                if movie_poster[i] != "Poster not available":
                    st.image(movie_poster[i])
                else:
                    st.write(movie_poster[i])
