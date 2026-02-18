from flask import Flask, render_template, request
import requests

app = Flask(__name__)


# Multi-source lyrics fetch function
def fetch_lyrics(artist, song):
    apis = [
        f"https://api.lyrics.ovh/v1/{artist}/{song}",
        f"https://lyrist.vercel.app/api/{artist}/{song}"
    ]

    for api in apis:
        try:
            response = requests.get(api, timeout=10)

            if response.status_code == 200:
                data = response.json()

                lyrics = data.get("lyrics") or data.get("lyric")
                if lyrics:
                    return lyrics

        except requests.exceptions.Timeout:
            continue
        except requests.exceptions.ConnectionError:
            continue

    return None


@app.route("/", methods=["GET", "POST"])
def home():
    lyrics = None
    artist = ""
    song = ""
    error = None

    if request.method == "POST":
        artist = request.form.get("artist", "").strip()
        song = request.form.get("song", "").strip()

        if not artist or not song:
            error = "Please enter artist and song."
        else:
            lyrics = fetch_lyrics(artist, song)

            if not lyrics:
                error = "Lyrics not found. Try simple song name."

    return render_template(
        "index.html",
        lyrics=lyrics,
        artist=artist,
        song=song,
        error=error
    )


# Important for Render / Gunicorn
if __name__ == "__main__":
    app.run()