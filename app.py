from flask import Flask, render_template_string, request
import re

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>🎵 jowelynmp3</title>
</head>
<body style="text-align: center; font-family: sans-serif;">
    <h2>🎵 Welcome to jowelynmp3 🎵</h2>
    <form method="POST">
        <input type="text" name="url" placeholder="Enter YouTube URL" style="width: 300px;" required>
        <br><br>
        <input type="submit" value="Convert to MP3">
    </form>

    {% if download_url %}
        <h3>Your MP3 is ready:</h3>
        <iframe src="{{ download_url }}" width="100%" height="100" style="border: none;"></iframe>
    {% endif %}
</body>
</html>
'''

def extract_video_id(url):
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    return match.group(1) if match else None

@app.route('/', methods=['GET', 'POST'])
def index():
    download_url = None
    if request.method == 'POST':
        yt_url = request.form['url']
        video_id = extract_video_id(yt_url)
        if video_id:
            download_url = f"https://api.vevioz.com/api/button/mp3/{video_id}"
    return render_template_string(HTML, download_url=download_url)

if __name__ == '__main__':
    app.run(debug=True)

