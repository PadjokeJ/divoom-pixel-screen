import requests
from os import getenv
from dotenv import load_dotenv
load_dotenv("local.env", verbose=True)
from io import BytesIO

hostname = "https://api.spotify.com/v1/"

spotify_token = getenv("SPOTIFY_TOKEN")
client_secret = getenv("SPOTIFY_SECRET")
client_id = getenv("SPOTIFY_ID")
auth_code = getenv("SPOTIFY_AUTHCODE")


headers = {"Authorization": f"Bearer {spotify_token}"}
s = requests.Session()
s.headers.update(headers)

def progress_bar():
    response = s.get(hostname + "me/player")
    if response.status_code == 200:
        res = response.json()

        progress = res["progress_ms"]
        max_duration = res["item"]["duration_ms"]

        image_url = res["item"]["album"]["images"][0]["url"]

        return (progress, max_duration, image_url, res["is_playing"])
    else:
        spotify_token = refresh_token()
        headers = {"Authorization": f"Bearer {spotify_token}"}
        s.headers.update(headers)
        return progress_bar()
    
def album_cover(url):
    response = s.get(url)
    return BytesIO(response.content)

def refresh_token():
    token_url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, headers=headers, data=f"grant_type=refresh_token&client_id={client_id}&client_secret={client_secret}&scope=user-read-playback-state user-modify-playback-state&refresh_token={auth_code}&redirect_uri=localhost:")
    return response.json()["access_token"]

if __name__ == "main":
    print()