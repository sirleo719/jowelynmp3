from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

API_HOST = "youtube-mp36.p.rapidapi.com"
API_KEY = "YOUR_RAPIDAPI_KEY"  # Replace this with your own RapidAPI key

HTML = '''
<!DOCTYPE html>
<html>
<head><title>🎵 jowelynmp3</title></head>
<body style="text-align:center; font-family:sans-serif;">
    <h2>🎵 Welcome to jowelynmp3 🎵</h2>
    <form method="post">
        <input type="text" name="url" placeholder="Enter YouTube URL" size="40" required>
        <input type="submit" value="Convert to MP3">
    </form>
    {% if download_url %}
        <p><strong>Your MP3 is ready:</strong></p>
        <a href="{{ download_url }}" target="_blank">🎧 Click here to download</a>
    {% elif error %}
        <p style="color:red;">{{ error }}</p>
    {% endif %}
</body>
</html>
'''

def extract_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    download_url = None
    error = None

    if request.method == "POST":
        url = request.form.get("url")
        video_id = extract_video_id(url)

        if not video_id:
            error = "Invalid YouTube URL"
        else:
            api_url = f"https://{API_HOST}/dl?id={video_id}"
            headers = {
                "X-RapidAPI-Key": API_KEY,
                "X-RapidAPI-Host": API_HOST,
            }
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "ok":
                    download_url = data.get("link")
                else:
                    error = "Conversion failed. Try another video."
            else:
                error = "API error. Try again later."

    return render_template_string(HTML, download_url=download_url, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
