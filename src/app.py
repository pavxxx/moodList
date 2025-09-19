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
try:
    user_info = sp.me()
    display_name = user_info.get("display_name", "Spotify User")
except Exception as e:
    st.error(f"Spotify authentication failed: {e}")
    st.stop()

# Streamlit UI
st.title(f"🎵 Welcome to MoodList, **{display_name}**!")
st.write("Use the sliders to set your mood and generate a playlist!")
st.markdown("---")

# Sliders for audio features
energy = st.slider("Energy", 0.0, 1.0, 0.5)
danceability = st.slider("Danceability", 0.0, 1.0, 0.5)
valence = st.slider("Valence (Happiness)", 0.0, 1.0, 0.5)

if st.button("Generate Playlist"):
    st.write("Fetching your top artists...")

    # Fetch user's top artists
    try:
        top_artists = sp.current_user_top_artists(limit=3)
        artist_ids = [artist['id'] for artist in top_artists['items']]
        st.write("Top artist IDs:", artist_ids)

        # Fallback if no top artists
        if not artist_ids:
            st.warning("No top artists found. Using default popular artist.")
            artist_ids = ["1Xyo4u8uXC1ZmMpatF05PJ"]  # The Weeknd

        # Limit seed artists to max 5
        seed_artists = artist_ids[:5]

        # Generate recommendations with error handling
        try:
            recommendations = sp.recommendations(
                seed_artists=seed_artists,
                limit=20,
                target_energy=energy,
                target_danceability=danceability,
                target_valence=valence
            )
        except spotipy.SpotifyException:
            st.warning("Could not generate recommendations with these artists. Using default popular artist.")
            seed_artists = ["1Xyo4u8uXC1ZmMpatF05PJ"]  # fallback
            recommendations = sp.recommendations(seed_artists=seed_artists, limit=20)

        # Get track URIs
        track_uris = [track['uri'] for track in recommendations['tracks']]
        if not track_uris:
            st.warning("No tracks generated. Try adjusting sliders or listening more on Spotify first.")
            st.stop()

        # Create playlist
        playlist = sp.user_playlist_create(
            user=user_info['id'],
            name="AI Generated Playlist",
            public=False
        )

        # Add tracks
        sp.playlist_add_items(playlist['id'], track_uris)

        # Success message and embedded player
        st.success(f"✅ Playlist created! [Open in Spotify]({playlist['external_urls']['spotify']})")
        st.markdown(f"""
        <iframe src="https://open.spotify.com/embed/playlist/{playlist['id']}" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
