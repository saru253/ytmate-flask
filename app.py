from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    if request.method == 'POST':
        url = request.form['url']
        quality = request.form.get('quality', 'best')
        try:
            ydl_opts = {
                'format': quality,
                'outtmpl': 'downloaded.%(ext)s',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            return send_file(filename, as_attachment=True)
        except Exception as e:
            output = f"Error: {str(e)}"
    return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
