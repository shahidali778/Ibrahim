import os
import re
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load API Key from environment variable
API_KEY = os.getenv("Youtube_API_Key")
if not API_KEY:
    raise ValueError("Error: Youtube_API_Key environment variable is missing!")

# Function to extract video ID from various YouTube URL formats
def extract_video_id(youtube_url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", youtube_url)
    return match.group(1) if match else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    youtube_url = request.form.get('youtube_url', '').strip()

    if not youtube_url:
        return jsonify({"error": "No URL provided"}), 400

    video_id = extract_video_id(youtube_url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    # Make API request to YouTube
    api_url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={API_KEY}&part=snippet"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            return jsonify(data)
        else:
            return jsonify({"error": "No video found for this ID"}), 404
    else:
        return jsonify({"error": f"YouTube API error: {response.status_code}"}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))  # Render provides PORT dynamically
    app.run(host="0.0.0.0", port=port, debug=False)
