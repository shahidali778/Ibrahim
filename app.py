from flask import Flask, request, render_template, send_file
from pytube import YouTube
import os

app = Flask(__name__)

# Ensure download directory exists
download_folder = "downloads"
os.makedirs(download_folder, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        video_url = request.form['url']
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        file_path = os.path.join(download_folder, yt.title + ".mp3")
        audio_stream.download(output_path=download_folder, filename=yt.title + ".mp3")
        
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
