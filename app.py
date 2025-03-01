@app.route('/convert', methods=['POST'])
def convert():
    youtube_url = request.form.get('youtube_url', '').strip()

    if not youtube_url:
        return jsonify({"error": "No URL provided"}), 400

    if "v=" in youtube_url:
        video_id = youtube_url.split("v=")[1].split("&")[0]
    else:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    api_url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={API_KEY}&part=snippet"
    response = requests.get(api_url)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch data"}), 500
