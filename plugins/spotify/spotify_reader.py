import requests
from os import getenv
from dotenv import load_dotenv
load_dotenv("../../local.env", verbose=True)
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

def get_auth_from_user():
    import requests
    import webbrowser

    redirect_uri = "http://localhost"

    # Request authorization from the user
    auth_url = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=user-read-playback-state user-modify-playback-state"
    response = requests.get(auth_url)

    # Open in browser, to log in to spotify
    webbrowser.open(response.url)

def get_token():
    import requests
    redirect_uri = "http://localhost"

    code = "Base64 code obtained from get_auth_from_user()"
    token_url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "authorization_code", "code": code, "redirect_uri": redirect_uri}
    response = requests.post(token_url, headers=headers, data=f"grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&scope=user-read-playback-state user-modify-playback-state&code={code}&redirect_uri={redirect_uri}")

    with open("spotify_tokens.json", 'wb') as fd:
        for chunk in response.iter_content(chunk_size=128):
            fd.write(chunk)

def refresh_token():
    token_url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, headers=headers, data=f"grant_type=refresh_token&client_id={client_id}&client_secret={client_secret}&scope=user-read-playback-state user-modify-playback-state&refresh_token={auth_code}&redirect_uri=localhost:")
    return response.json()["access_token"]

if __name__ == "main":
    print()