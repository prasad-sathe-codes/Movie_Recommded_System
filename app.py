import streamlit as st
import pickle
import requests

# OMDb API Key
API_KEY = "bf9a1b19"

# Load movie list and similarity data
with open("movie_list.pkl", "rb") as file:
    movie_list = pickle.load(file)

with open("similarity.pkl", "rb") as file:
    similarity = pickle.load(file)

# Function to fetch movie poster from OMDb API
# Define a function to get the movie poster
def get_movie_poster(movie_name):
    # Create a URL to access the OMDB API with the movie name and API key
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"
    # Make a GET request to the URL and convert the response to JSON
    response = requests.get(url).json()
    # Return the poster URL from the JSON response, or None if it doesn't exist
    return response.get("Poster", None)

# Function to recommend movies with posters
def recommend(movie):
    # Get the index of the movie in the movie_list
    index = movie_list[movie_list["title"] == movie].index[0]
    # Get the similarity scores of the movie with all other movies
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movies = []
    for i in distances[1:6]:  # Get top 5 recommendations
        title = movie_list.iloc[i[0]].title
        poster_url = get_movie_poster(title)  # Fetch poster
        recommended_movies.append((title, poster_url))
    
    return recommended_movies

# Streamlit UI
st.title("Movie Recommender System App ")

selected_movie = st.selectbox("Select the movie", movie_list["title"].values)

if st.button("Recommend"):
    recommended_movies = recommend(selected_movie)
    st.subheader("Recommended Movies:")

    cols = st.columns(5)  # Create 5 columns for movies

    for idx, (name, poster) in enumerate(recommended_movies):
        with cols[idx]:  # Display in separate columns
            st.text(name)
            if poster:
                st.image(poster, use_container_width=True)  # Fixed here
            else:
                st.write("No poster found")
