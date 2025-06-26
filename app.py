from flask import Flask, request, render_template, send_file
import requests

app = Flask(__name__)

RAPIDAPI_KEY = "523ad5b9b0msh1287a5b840d67f8p1fcd33jsn0dd086c55ee2"  # Your actual key

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['url']
    
    api_url = "https://yt-api-video-download.p.rapidapi.com/dl"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "yt-api-video-download.p.rapidapi.com"
    }
    params = {"url": video_url}

    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # Try to find an audio-only stream
        for link in data.get("link", []):
            if "audio" in link.get("type", "").lower():
                return f"<a href='{link['url']}' download>Click here to download MP3</a>"

        return "No audio found. Try a different video."

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
