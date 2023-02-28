import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import requests

movies = pd.read_csv('Datasets/final_data.csv')
# creating a count matrix
cv = CountVectorizer()
count_matrix = cv.fit_transform(movies['comb'])
# creating a similarity score matrix
similarity = cosine_similarity(count_matrix)

def fetch_poster(movie_title):
    url = "http://www.omdbapi.com/?i=tt3896198&apikey=88c55f79&t={}".format(movie_title)
    data = requests.get(url)
    data = data.json()
    poster_path = data['Poster']
    return poster_path 

def fetch_rating(movie_title):
    url = "http://www.omdbapi.com/?i=tt3896198&apikey=88c55f79&t={}".format(movie_title)
    data = requests.get(url)
    data = data.json()
    rating = data['imdbRating']
    return rating

def recommend(movie):
    movie = movie.lower()
    movie_index = movies[movies['movie_title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)) , reverse=True , key=lambda x: x[1])[1:6]
    
    recommended_movie_names = []
    recommended_movie_ratings = []
    recommended_movie_posters = []
    
    
    for i in movies_list:
        movie_title = movies.iloc[i[0]].movie_title
        recommended_movie_ratings.append(fetch_rating(movie_title))
        recommended_movie_posters.append(fetch_poster(movie_title))
        recommended_movie_names.append(movie_title.capitalize())
        
    return recommended_movie_posters,recommended_movie_names,recommended_movie_ratings
        
        
#movies = pickle.load(open('movies.pkl','rb'))


#similarity = pickle.load(open('similarity.pkl','rb'))


st.title('Movie Recommendation System')


selected_movie_name = st.selectbox(
    'Type or Select a Movie from dropdown',
    (movies['movie_title'].str.capitalize().values))

if st.button('Show Recommendations'):
    recommended_movie_posters,recommended_movie_names,recommended_movie_ratings = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.text('Rating: '+recommended_movie_ratings[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.text('Rating: '+recommended_movie_ratings[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.text('Rating: '+recommended_movie_ratings[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.text('Rating: '+recommended_movie_ratings[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.text('Rating: '+recommended_movie_ratings[4])
        st.image(recommended_movie_posters[4])