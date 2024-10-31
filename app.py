### if i install packages without creating a virtual environment, it will be installed globally 
### and will be available to all the projects. But if i create a virtual environment,
###  the packages will be installed locally for this project only.

# i can use pickle not just for df  , but also for any python onjects like list, dict, etc
import streamlit as st 
import pandas as pd
import pickle
import numpy as np
import requests
import os 
import gdown

with open('movies.pkl', 'rb') as file:
    df = pickle.load(file)
    # i can use this df and use normal dataframe operations

def download_file_from_google_drive(file_id, local_file_path):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    gdown.download(url, local_file_path, quiet=False)

# Define the Google Drive file ID and local file path
file_id = '1cSBwkJ6-ADDBgq2EQN0trUx7d9XW3Apq'
local_file_path = 'similarity.pkl'


# Download the file if it doesn't exist locally
if not os.path.exists(local_file_path):
    download_file_from_google_drive(file_id, local_file_path)



with open(local_file_path, 'rb') as file:
    similarity = pickle.load(file)


movies_list = df['title'].values


def poster_fetch(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3MzQ0YmVjZTQ3ZTQ5NDU2NDA2YzY2M2I1ZGVmZDA1ZCIsIm5iZiI6MTczMDMwNzY2OC4wNTUyNTIsInN1YiI6IjY3MjI2NTZlOTc0YTY3NmM2ZGYzNTczMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.4eGebmXr8yj4YN3z7QvTyy7W2LSfoHEl9JPQW3OMtCg"
}
    response = requests.get(url, headers=headers)
    data = response.json() 
    if data['belongs_to_collection']:
         return 'http://image.tmdb.org/t/p/w500/' + data['belongs_to_collection']['poster_path']
    else:
        return 'https://www.thermaxglobal.com/wp-content/uploads/2020/05/image-not-found.jpg'
   



def recommend(movie):
    """it is the clicked movie, now provide recommendations based on it"""
    movie_index = df[df['title']==movie].index[0]
    similarities = similarity[movie_index]
    movies_list_indices = np.argsort(similarities)[::-1][1:6]
    
    recommended_movies = []
    recommended_posters = []
    
    for item in movies_list_indices:
        recommended_movies.append(df.loc[item].title)
        recommended_posters.append(poster_fetch(df.loc[item].movie_id))
    return recommended_movies,recommended_posters
    




st.title('Movie recommendor system')


# Dropdown menu
options = movies_list
selected_option = st.selectbox("Choose an option:", options)


# Display selected option
st.write("You selected:", selected_option)

# we want images in a certain grid

if st.button("Recommend"):  # if the button is clicked
    names,posters = recommend(selected_option)
    
     # Create columns for the grid layout
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            # st.image to display the image
            st.image(posters[i], caption=names[i])







# requirements.txt contains list of all packages needed, which will be needed to install in the virtual environment of server