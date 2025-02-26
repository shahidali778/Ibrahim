import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = os.getenv("AIzaSyD9OGlbU8eU5O4AAVeizGwVpeEzTjC9O6A")

@app.route('/')
def index():
    return render_template('index.html')  # Ensure index.html exists inside a templates/ folder

@app.route('/convert', methods=['POST'])
def convert():
    youtube_url = request.form.get('youtube_url')

    if not youtube_url:
        return jsonify({"error": "No URL provided"}), 400

    api_url = f"https://www.googleapis.com/youtube/v3/videos?id={youtube_url}&key={API_KEY}&part=snippet"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch data"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Use Render's detected port
    app.run(host='0.0.0.0', port=port)

  
