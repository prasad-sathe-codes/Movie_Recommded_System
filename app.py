import streamlit as st
import pickle

# Load movie list and similarity data
with open("movie_list.pkl", "rb") as file:
    movie_list = pickle.load(file)

with open("similarity.pkl", "rb") as file:
    similarity = pickle.load(file)

# Function to recommend movies
def recommend(movie):
    index = movie_list[movie_list["title"] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies_name = []
    for i in distances[1:6]:  # Get top 5 recommendations
        recommended_movies_name.append(movie_list.iloc[i[0]].title)
    return recommended_movies_name

# Streamlit UI
st.title("Movie Recommender System")
selected_movie = st.selectbox("Select the movie", movie_list["title"].values)

if st.button("Recommend"):
    recommended_movies_name = recommend(selected_movie)
    st.subheader("Recommended Movies:")
    for name in recommended_movies_name:
        st.write(name)
