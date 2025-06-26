from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>🎵 jowelynmp3 🎵</title>
</head>
<body style="text-align: center; font-family: sans-serif; padding-top: 50px;">
    <h1>🎵 Welcome to jowelynmp3 🎵</h1>
    <form method="POST">
        <input type="text" name="url" placeholder="Enter YouTube URL" size="50" required>
        <br><br>
        <input type="submit" value="Convert to MP3">
    </form>

    {% if video_id %}
        <h2>Your MP3 is ready:</h2>
        <iframe src="https://api.vevioz.com/api/button/mp3/{{ video_id }}" width="100%" height="60" frameborder="0" allowtransparency="true" scrolling="no" style="border:none;"></iframe>
    {% endif %}
</body>
</html>
'''

def extract_video_id(url):
    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    video_id = None
    if request.method == 'POST':
        url = request.form['url']
        video_id = extract_video_id(url)
    return render_template_string(HTML, video_id=video_id)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
