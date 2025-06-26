from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Replace this with your actual X-RapidAPI-Key
RAPIDAPI_KEY = "523ad5b9b0msh1287a5b840d67f8p1fcd33jsn0dd086c55ee2"

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>🎵 JowelynMP3 Downloader 🎵</title>
</head>
<body>
    <div style="text-align:center;">
        <h1>🎵 Welcome to JowelynMP3 🎵</h1>
        <form method="post">
            <input name="url" placeholder="Enter YouTube URL" size="50" required>
            <input type="submit" value="Download MP3">
        </form>
        {% if error %}
            <p style="color:red;">{{ error }}</p>
        {% elif mp3_url %}
            <p>Your MP3 is ready:</p>
            <a href="{{ mp3_url }}" target="_blank">Click here to download</a>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    mp3_url = None
    error = None
    if request.method == 'POST':
        youtube_url = request.form['url']
        url = "https://yt-api-video-download.p.rapidapi.com/dl"

        querystring = {"url": youtube_url}

        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "yt-api-video-download.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()
            mp3_options = data.get("link", [])
            mp3_url = next((x["url"] for x in mp3_options if x["type"] == "audio"), None)
            if not mp3_url:
                error = "No audio found. Try a different video."
        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template_string(HTML, mp3_url=mp3_url, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
