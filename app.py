from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# 🔑 Replace this with your actual API key from RapidAPI
RAPIDAPI_KEY = "523ad5b9b0msh1287a5b840d67f8p1fcd33jsn0dd086c55ee2"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        video_url = request.form['url']
        video_id = video_url.split("v=")[-1].split("&")[0] if "v=" in video_url else video_url.split("/")[-1]

        api_url = "https://yt-api-video-download.p.rapidapi.com/dl"
        querystring = {"id": video_id}
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "yt-api-video-download.p.rapidapi.com"
        }

        response = requests.get(api_url, headers=headers, params=querystring)
        data = response.json()

        try:
            audio_link = data['link']['mp3']['mp3128']['url']
            return render_template('index.html', download_link=audio_link)
        except Exception as e:
            return render_template('index.html', error="No audio found or error occurred.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
