import os
from dotenv import load_dotenv
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load secrets from .env
load_dotenv()

# Spotify API auth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-top-read playlist-modify-private playlist-modify-public"
))

# Get user info
user_info = sp.me()
display_name = user_info.get("display_name", "Spotify User")

# Streamlit UI
st.title(f"Welcome to MoodList , **{display_name}**!")
st.write(f"A Personalized Spotify Playlist Generator")
st.write(f"Logged in as **{display_name}**")

# Sliders for audio features
energy = st.slider("Energy", 0.0, 1.0, 0.5)
danceability = st.slider("Danceability", 0.0, 1.0, 0.5)
valence = st.slider("Valence (Happiness)", 0.0, 1.0, 0.5)

if st.button("Generate Playlist"):
    st.write("Fetching your top artists...")

    # Fetch user’s top artists
    top_artists = sp.current_user_top_artists(limit=3)
    if not top_artists['items']:
        st.error("No top artists found. Try listening more on Spotify first 🎧")
    else:
        artist_ids = [artist['id'] for artist in top_artists['items']]

        # Get recommendations
        recommendations = sp.recommendations(
            seed_artists=artist_ids,
            limit=20,
            target_energy=energy,
            target_danceability=danceability,
            target_valence=valence
        )

        # Create playlist
        user_id = user_info['id']
        playlist = sp.user_playlist_create(
            user=user_id,
            name="AI Generated Playlist",
            public=False
        )

        # Add tracks
        track_uris = [track['uri'] for track in recommendations['tracks']]
        if track_uris:
            sp.playlist_add_items(playlist['id'], track_uris)
            st.success(f"✅ Playlist created! [Open in Spotify]({playlist['external_urls']['spotify']})")
        else:
            st.warning("No tracks were generated. Try adjusting the sliders.")
