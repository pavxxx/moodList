import os
from dotenv import load_dotenv
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image

# Load environment variables
load_dotenv()

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-top-read playlist-modify-private playlist-modify-public"
))

# Get user info
try:
    user_info = sp.me()
    display_name = user_info.get("display_name", "Spotify User")
except Exception as e:
    st.error(f"Spotify authentication failed: {e}")
    st.stop()

# ---------------- UI ----------------
# Banner image (optional, put a banner in assets/banner.png)
try:
    banner = Image.open("assets/banner.png")
    st.image(banner, use_column_width=True)
except:
    pass  # skip if no image

st.title(f"🎵 Welcome to MoodList, **{display_name}**!")
st.write("Set your mood using the sliders below and generate a playlist!")
st.markdown("---")

# Mood sliders
st.subheader("🎚️ Mood Settings")
energy = st.slider("Energy ⚡", 0.0, 1.0, 0.5)
danceability = st.slider("Danceability 💃", 0.0, 1.0, 0.5)
valence = st.slider("Valence (Happiness 😄)", 0.0, 1.0, 0.5)

st.markdown("---")

# Generate Playlist Button
if st.button("🎶 Generate Playlist"):
    st.info("Creating your playlist...")

    try:
        # ---------------- Fallback tracks ----------------
        track_uris = [
            "spotify:track:7lPN2DXiMsVn7XUKtOW1CS",  # Blinding Lights - The Weeknd
            "spotify:track:3KkXRkHbMCARz0aVfEt68P",  # Levitating - Dua Lipa
            "spotify:track:2takcwOaAZWiXQijPHIx7B"   # Save Your Tears - The Weeknd
        ]

        # Create private playlist
        playlist = sp.user_playlist_create(
            user=user_info['id'],
            name="AI Generated Playlist",
            public=False
        )

        # Add tracks
        sp.playlist_add_items(playlist['id'], track_uris)

        # ---------------- Success UI ----------------
        st.success(f"✅ Playlist created! [Open in Spotify]({playlist['external_urls']['spotify']})")
        st.markdown("---")
        st.subheader("🎧 Tracks in your playlist:")

        for idx, uri in enumerate(track_uris, start=1):
            track = sp.track(uri)
            st.write(f"{idx}. {track['name']} — {track['artists'][0]['name']}")

    except spotipy.SpotifyException as e:
        st.error(f"Spotify API error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
