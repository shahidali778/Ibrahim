from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

# Ensure download directory exists
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    try:
        video_url = request.form["url"]
        yt = YouTube(video_url)
        
        # Get the best audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        file_path = audio_stream.download(output_path=DOWNLOAD_FOLDER)
        
        # Rename to .mp3
        mp3_path = file_path.replace(".mp4", ".mp3").replace(".webm", ".mp3")
        os.rename(file_path, mp3_path)
        
        return send_file(mp3_path, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
