from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# 🔐 Replace with your actual RapidAPI Key
RAPIDAPI_KEY = "523ad5b9b0msh1287a5b840d67f8p1fcd33jsn0dd086c55ee2"

def get_audio_url(youtube_url):
    try:
        # Extract the video ID from the URL
        if "watch?v=" in youtube_url:
            video_id = youtube_url.split("v=")[-1].split("&")[0]
        elif "youtu.be/" in youtube_url:
            video_id = youtube_url.split("/")[-1].split("?")[0]
        else:
            return None

        url = "https://yt-api-video-download.p.rapidapi.com/dl"
        querystring = {"id": video_id}
        headers = {
            "X-RapidAPI-Key": "X-RapidAPI-Key": "523ad5b9b0msh1287a5b840d67f8p1fcd33jsn0dd086c55ee2",
,
            "X-RapidAPI-Host": "yt-api-video-download.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            data = response.json()
            for audio in data.get("audios", []):
                if ".mp3" in audio["url"]:
                    return audio["url"]
            return None
        else:
            print("API error:", response.status_code, response.text)
            return None
    except Exception as e:
        print("Error:", e)
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    audio_url = None
    error = None
    if request.method == "POST":
        youtube_url = request.form.get("url")
        if youtube_url:
            audio_url = get_audio_url(youtube_url)
            if not audio_url:
                error = "No audio found or video requires login. Try another link."
    return render_template("index.html", audio_url=audio_url, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

