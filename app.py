from flask import Flask

app = Flask(__name__)

import re

def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None

@app.route('/convert', methods=['POST'])
def convert():
    youtube_url = request.form.get('youtube_url')

    if not youtube_url:
        return jsonify({"error": "No URL provided"}), 400

    video_id = extract_video_id(youtube_url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    api_url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={AIzaSyD9OGlbU8eU5O4AAVeizGwVpeEzTjC9O6A}&part=snippet"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        if not data["items"]:  # Check if no results
            return jsonify({"error": "No video found for this ID"}), 404
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch data"}), 500

