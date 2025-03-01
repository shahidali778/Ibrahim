import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Load API Key from environment variable
API_KEY = os.getenv("AIzaSyD9OGlbU8eU5O4AAVeizGwVpeEzTjC9O6A")  # Ensure this is set in PythonAnywhere

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    youtube_url = request.form.get('youtube_url', '').strip()

    if not youtube_url:
        return jsonify({"error": "No URL provided"}), 400

    # Extract video ID from URL
    video_id = extract_video_id(youtube_url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    # Fetch video details using YouTube API
    api_url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={API_KEY}&part=snippet"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch data"}), 500

def extract_video_id(url):
    """Extracts the YouTube video ID from various URL formats."""
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    elif "v=" in url:
        return url.split("v=")[1].split("&")[0]
    return None

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))  # Render provides PORT dynamically
    app.run(host="0.0.0.0", port=port, debug=False)
