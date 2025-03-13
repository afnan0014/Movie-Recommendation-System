import streamlit as st
import pickle
import pandas as pd
import requests

# API Integration

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):

    movies_index=movies[movies['title']== movie].index[0]
    distances=similarity[movies_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:16]
    recommended_movies=[]
    recommended_movies_posters=[]

    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        #fetch posters from api
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
        
    return recommended_movies,recommended_movies_posters


movies_list=pickle.load(open('movies.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))

movies=pd.DataFrame(movies_list)
st.title('Movie Recommender System')
selected_movie_name=st.selectbox('Select Your Movie',movies['title'].values)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    # col1, col2, col3, col4, col5,col6,col7 = st.columns(7)
    # with col1:
    #     st.text(recommended_movie_names[0])
    #     st.image(recommended_movie_posters[0])
    # with col2:
    #     st.text(recommended_movie_names[1])
    #     st.image(recommended_movie_posters[1])

    # with col3:
    #     st.text(recommended_movie_names[2])
    #     st.image(recommended_movie_posters[2])
    # with col4:
    #     st.text(recommended_movie_names[3])
    #     st.image(recommended_movie_posters[3])
    # with col5:
    #     st.text(recommended_movie_names[4])
    #     st.image(recommended_movie_posters[4])
    # with col6:
    #     st.text(recommended_movie_names[5])
    #     st.image(recommended_movie_posters[5])
    # with col7:
    #     st.text(recommended_movie_names[6])
    #     st.image(recommended_movie_posters[6])

    # num_recommendations = 10
    # cols = st.columns(num_recommendations)

    # for idx, col in enumerate(cols):
    #     with col:
    #         st.text(recommended_movie_names[idx])
    #         st.image(recommended_movie_posters[idx])




    # Total number of movie recommendations available
    num_recommendations = 15

    # Number of movies to display per row
    movies_per_row = 5

    # Loop through the recommendations in steps of 'movies_per_row'
    # This ensures that each iteration handles one row of movies
    for i in range(0, num_recommendations, movies_per_row):
        
        # Create columns for the current row
        # This will generate 7 columns side by side
        cols = st.columns(movies_per_row)
        
        # Loop through each column and its index
        for idx, col in enumerate(cols):
            
            # Calculate the actual index of the movie in the list
            movie_index = i + idx
            
            # Check if the movie index is within the total available movies
            # This avoids errors if the list has fewer items than expected
            if movie_index < len(recommended_movie_names):
                
                # Place content inside the current column
                with col:
                    # Display the movie name
                    st.text(recommended_movie_names[movie_index])
                    
                    # Display the movie poster image
                    st.image(recommended_movie_posters[movie_index])
