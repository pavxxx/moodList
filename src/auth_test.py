import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load env vars
load_dotenv()

CLIENT_ID = os.getenv("998e889a3e9248b1be7836a558c0e481")
CLIENT_SECRET = os.getenv("d107da683037401eb706428de10225e2")
REDIRECT_URI = os.getenv("http://127.0.0.1:8888/callback")

scope = "user-top-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="998e889a3e9248b1be7836a558c0e481",
    client_secret="d107da683037401eb706428de10225e2",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope=scope
))

# Test: Get user profile
me = sp.me()
print("Logged in as:", me['display_name'])
