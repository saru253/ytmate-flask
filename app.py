
from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    if request.method == 'POST':
        url = request.form['url']
        format = request.form['format']
        ydl_opts = {}

        if format == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            }
        elif format == 'mp4_360':
            ydl_opts = {'format': '18'}
        elif format == 'mp4_480':
            ydl_opts = {'format': '135+140'}
        elif format == 'mp4_720':
            ydl_opts = {'format': '22'}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            output = "✅ Download complete. Check server files."
        except Exception as e:
            output = "❌ Failed to download. " + str(e)
    return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
