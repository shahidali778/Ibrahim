from flask import Flask, request, jsonify, send_file
import os
import requests
from pytube import YouTube

app = Flask(__name__)

# Set the download folder
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# ✅ Add your YouTube API Key here
YOUTUBE_API_KEY = "AIzaSyD9OGlbU8eU5O4AAVeizGwVpeEzTjC9O6A"  # Replace with your actual API key

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "YouTube to MP3 Converter is running!"})

@app.route("/convert", methods=["POST"])
def convert():
    try:
        # ✅ Check if URL is provided
        data = request.json
        if not data or "url" not in data:
            return jsonify({"error": "Missing 'url' parameter"}), 400

        youtube_url = data["url"]
        video_id = youtube_url.split("v=")[-1].split("&")[0]  # Extract video ID

        # ✅ Fetch video details using YouTube API
        api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YOUTUBE_API_KEY}"
        response = requests.get(api_url)
        video_data = response.json()

        if "items" not in video_data or len(video_data["items"]) == 0:
            return jsonify({"error": "Invalid YouTube video URL"}), 400

        video_title = video_data["items"][0]["snippet"]["title"]

        # ✅ Download audio using pytube
        yt = YouTube(youtube_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            return jsonify({"error": "No audio stream found"}), 500

        output_path = audio_stream.download(output_path=DOWNLOAD_FOLDER)
        
        # ✅ Rename file to .mp3
        base, ext = os.path.splitext(output_path)
        mp3_filename = f"{base}.mp3"
        os.rename(output_path, mp3_filename)

        return jsonify({
            "message": "Download successful",
            "title": video_title,
            "file": mp3_filename
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    try:
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=True)
