from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

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
        <h2>🎵 Welcome to jowelynmp3 🎵</h2>
        <form method="post">
            Enter YouTube URL: <input type="text" name="url" required>
            <input type="submit" value="Download MP3">
        </form>
        {% if filename %}
            <p>Your MP3 is ready: <a href="/download/{{ filename }}">Click here to download</a></p>
        {% elif error %}
            <p style="color: red;">Error: {{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    filename = None
    error = None
    if request.method == 'POST':
        url = request.form['url']
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
            error = str(e)
    return render_template_string(HTML, filename=filename, error=error)

@app.route('/download/<filename>')
def download(filename):
    return send_file(f"{DOWNLOAD_DIR}/{filename}", as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port
    app.run(host='0.0.0.0', port=port, debug=False)
    
