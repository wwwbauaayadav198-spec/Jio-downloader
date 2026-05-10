import os
from flask import Flask, request, send_file
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <div style="text-align:center; padding:50px; font-family:Arial;">
        <h2 style="color:red;">My Jio Downloader</h2>
        <form action="/download" method="get">
            <input type="text" name="q" placeholder="Gaane ka naam ya YouTube link..." style="width:80%; padding:10px;"><br><br>
            <button name="f" value="144" style="background:#2196F3; color:white; padding:10px; width:100%;">Download 144p</button><br><br>
            <button name="f" value="240" style="background:#4CAF50; color:white; padding:10px; width:100%;">Download 240p</button><br><br>
            <button name="f" value="mp3" style="background:#FF9800; color:white; padding:10px; width:100%;">Download MP3</button>
        </form>
    </div>
    '''

@app.route('/download')
def download():
    query = request.args.get('q')
    f = request.args.get('f')
    
    ydl_opts = {
        'format': 'bestaudio/best' if f == 'mp3' else f'best[height<={f}]',
        'outtmpl': 'file.%(ext)s',
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_query = f"ytsearch1:{query}" if "youtube.com" not in query else query
            info = ydl.extract_info(search_query, download=True)
            filename = ydl.prepare_filename(info.get('entries', [info])[0])
            return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
