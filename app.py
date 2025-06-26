from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>jowelynmp3</title>
</head>
<body>
    <div style="text-align: center; font-family: Arial, sans-serif;">
        <h1>🎵 Welcome to jowelynmp3 🎵</h1>
        <form method="post">
            <input type="text" name="url" placeholder="Enter YouTube URL" size="50" required>
            <br><br>
            <input type="submit" value="Get MP3 Link">
        </form>

        {% if download_url %}
            <h3>Your MP3 is ready:</h3>
            <a href="{{ download_url }}" target="_blank">Click here to download</a>
        {% elif error %}
            <p style="color: red;">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
'''

def extract_video_id(url):
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    download_url = None
    error = None
    if request.method == 'POST':
        url = request.form.get('url')
        video_id = extract_video_id(url)
        if video_id:
            download_url = f"https://yt-download.org/api/widget/mp3/{video_id}"
        else:
            error = "Invalid YouTube URL. Please try again."
    return render_template_string(HTML, download_url=download_url, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

