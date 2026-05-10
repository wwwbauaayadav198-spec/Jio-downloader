from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

HTML_TEMPLATE = '''
<html>
<body style="font-family:sans-serif; text-align:center; padding:15px; background:#f0f0f0;">
    <div style="background:#fff; padding:15px; border-radius:10px; border: 2px solid red;">
        <h2 style="color:red;">My Jio Downloader</h2>
        <form action="/process" method="get">
            <input type="text" name="q" placeholder="Gaane ka naam" style="width:90%; padding:10px;"><br><br>
            <button type="submit" name="f" value="144p" style="width:100%; padding:12px; background:#2196F3; color:white; border:none; margin-bottom:8px;">Download 3GP 144p</button>
            <button type="submit" name="f" value="240p" style="width:100%; padding:12px; background:#4CAF50; color:white; border:none; margin-bottom:8px;">Download 3GP 240p</button>
            <button type="submit" name="f" value="mp3" style="width:100%; padding:12px; background:#FF9800; color:white; border:none;">Download MP3</button>
        </form>
    </div>
    <p style="font-size:12px;">Link dalne ke baad thoda intezar karein...</p>
</body>
</html>
'''

@app.route('/')
def index(): return HTML_TEMPLATE

@app.route('/process')
def process():
    query = request.args.get('q')
    format_choice = request.args.get('f')
    if not query: return "Naam likho!"
    search = f"ytsearch1:{query}" if "youtu" not in query else query
    
    if format_choice == "144p":
        opts = {'format': '17', 'outtmpl': 'vid.3gp'}
        ext = 'vid.3gp'
    elif format_choice == "240p":
        opts = {'format': '36/best[ext=3gp]', 'outtmpl': 'vid.3gp'}
        ext = 'vid.3gp'
    else:
        opts = {'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '128'}], 'outtmpl': 'aud.mp3'}
        ext = 'aud.mp3'

    try:
        if os.path.exists(ext): os.remove(ext)
        with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([search])
        return send_file(ext, as_attachment=True)
    except Exception as e: return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
