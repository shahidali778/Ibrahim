import requests

url = "https://youtube-mp3-audio-video-downloader.p.rapidapi.com/get_m4a_download_link/rVQ2i8q2Y9A"

headers = {
	"x-rapidapi-key": "e84fa4ff88msh663872a4ba21b5dp1ff130jsn140078e2f696",
	"x-rapidapi-host": "youtube-mp3-audio-video-downloader.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())
