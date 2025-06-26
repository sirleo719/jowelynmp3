from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os
import re

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>jowelynmp3</title>
</head>
<body>
    <div style="text-align: center;">
        <img src="/static/logo.png" width="150">
        <h2>Welcome to jowelynmp3</h2>
        <form method="post">
            YouTube URL: <input type="text" name="url" required>
            <input type="submit" value="Download MP3">
        </form>
        {% if filename %}
            <p>Download ready: <a href="/download/{{ filename }}">Click here</a></p>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    filename = None
    if request.method == 'POST':
        yt_url = request.form['url']
        video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", yt_url)

        if not video_id_match:
            return "Invalid YouTube URL", 400

        video_id = video_id_match.group(1)
        url = f"https://yewtu.be/watch?v={video_id}"  # Or try another Invidious instance

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = f"{info['title']}.mp3"
        except Exception as e:
            return f"Download failed: {str(e)}", 500

    return render_template_string(HTML, filename=filename)

@app.route('/download/<filename>')
def download(filename):
    return send_file(f"{DOWNLOAD_DIR}/{filename}", as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

