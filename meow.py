import pickle
import streamlit as st
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def recommend_books():
    st.subheader("Book Recommendation System")
    model = pickle.load(open('model.pkl','rb'))
    book_names = pickle.load(open('books_name.pkl','rb'))
    final_rating = pickle.load(open('final_rating.pkl','rb'))
    pivot = pickle.load(open('pivot.pkl','rb'))





    def fetch_poster(suggestion):
        book_name = []
        ids_index = []
    

        for book_id in suggestion:
          book_name.append(pivot.index[book_id])

        for name in book_name[0]: 
         ids = np.where(final_rating['"Book-Title"'] == name)[0][0]
         ids_index.append(ids)

    # for idx in ids_index:
    #     url = final_rating.iloc[idx]['"Image-URL-L"']
    #     poster_url.append(url)

        return ids_index



    def recommend_book(book_name):
      books_list = []
      book_id = np.where(pivot.index == book_name)[0][0]
      distance, suggestion = model.kneighbors(pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6 )

    # poster_url = fetch_poster(suggestion)
    
      for i in range(len(suggestion)):
            books = pivot.index[suggestion[i]]
            for j in books:
                books_list.append(j)
            return books_list 
     



    selected_books = st.selectbox(
     "Type or select a book from the dropdown",
      book_names
    )
    
    
    recommended_books = []


    if st.button('Recommendation for you'):
      recommended_books = recommend_book(selected_books)
      if recommended_books and len(recommended_books) >= 6:
        col1, col2, col3, col4, col5 = st.columns(5)
      with col1:
        st.text(recommended_books[1])
        # st.image(poster_url[1])
      with col2:
        st.text(recommended_books[2])
        # st.image(poster_url[2])

      with col3:
        st.text(recommended_books[3])
        # st.image(poster_url[3])
      with col4:
        st.text(recommended_books[4])
        # st.image(poster_url[4])
      with col5:
        st.text(recommended_books[5])
        # st.image(poster_url[5])


def recommend_movies():
    st.subheader("Movie Recommendation System")

    def recommend(movie):
        try:
            index = movies[movies['title'] == movie].index[0]
            distances = sorted(
                list(enumerate(similarity[index])),
                reverse=True,
                key=lambda x: x[1]
            )
            recommended_movie_names = []
            for i in distances[1:6]:
                recommended_movie_names.append(movies.iloc[i[0]].title)
            return recommended_movie_names
        except Exception as e:
            st.error(f"Error: {e}")
            return []

    # Load movie data
    try:
        movies = pickle.load(open('movie_list.pkl', 'rb'))
        similarity = pickle.load(open('similarity.pkl', 'rb'))
    except FileNotFoundError as e:
        st.error(f"File not found: {e}")
        return
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return

    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )

    if st.button("Show Recommendation"):
        recommended_movie_names = recommend(selected_movie)
        if recommended_movie_names:
            st.write("Recommended Movies:")
            for movie in recommended_movie_names:
                st.write(f"- {movie}")
        else:
            st.warning("No recommendations available.")



def recommend_songs():
    st.subheader("Music Recommendation System")
    try:
        # Load music data and similarity model
        music = pickle.load(open("df.pkl", "rb"))
        similarity = pickle.load(open("ksimilarity.pkl", "rb"))

        # Helper function to fetch song album cover URL
        def get_song_album_cover_url(song_name, artist_name):
            try:
                search_query = f"track:{song_name} artist:{artist_name}"
                results = sp.search(q=search_query, type="track", limit=1)
                if results["tracks"]["items"]:
                    return results["tracks"]["items"][0]["album"]["images"][0]["url"]
                return "https://i.postimg.cc/0QNxYz4V/social.png"  # Default image if not found
            except:
                return "https://i.postimg.cc/0QNxYz4V/social.png"  # Fallback image

        # Function to get song recommendations
        def recommend(song):
            index = music[music["song"] == song].index[0]
            distances = sorted(
                list(enumerate(similarity[index])),
                reverse=True,
                key=lambda x: x[1]
            )
            recommended_songs = []
            recommended_posters = []
            for i in distances[1:6]:  # Top 5 recommendations
                song_name = music.iloc[i[0]].song
                artist = music.iloc[i[0]].artist
                poster_url = get_song_album_cover_url(song_name, artist)
                recommended_songs.append(song_name)
                recommended_posters.append(poster_url)
            return recommended_songs, recommended_posters

        # Streamlit UI for selecting a song
        music_list = music["song"].values
        selected_song = st.selectbox("Select a song", music_list)

        if st.button("Recommend Songs"):
            # Fetch recommendations
            recommended_songs, recommended_posters = recommend(selected_song)
            st.write("Recommended Songs:")
            
            # Display recommendations in columns
            cols = st.columns(5)
            for i, col in enumerate(cols):
                if i < len(recommended_songs):
                    with col:
                        st.text(recommended_songs[i])
                        st.image(recommended_posters[i])
    except Exception as e:
        st.error(f"Error: {e}")


        
            
        
            
            
        
def recommend_diseases():
    st.subheader("Disease Information System")
    st.write("Enter a symptom or condition to get disease information.")
    symptom = st.text_input("Enter symptom:")
    if symptom:
        st.write(f"Based on the symptom '{symptom}', here are possible conditions:")
        diseases = {"fever": ["Flu", "COVID-19", "Malaria"], "cough": ["Cold", "Bronchitis", "Asthma"],
                    "itching": ["psoriasis","dry skin (xerosis)","eczema (dermatitis)"]}
        st.write(diseases.get(symptom.lower(), ["No matching conditions found."]))

# Main App
st.title("Personalized Recommendation System")

st.write("Welcome! Choose a category to explore recommendations or information:")

with st.sidebar:
    st.subheader("Navigation")
    selection = st.radio("Go to:", ("Books", "Movies", "Songs", "Diseases"))

if selection == "Books":
    recommend_books()
elif selection == "Movies":
    recommend_movies()
elif selection == "Songs":
    recommend_songs()
elif selection == "Diseases":
    recommend_diseases()
