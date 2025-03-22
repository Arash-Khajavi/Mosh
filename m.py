requests
from flask import Flask, render_template, request
import os
app = Flask(__name__)

API_KEY = os.getenev("Youtube")
API_URL = "https://www.googleapis.com/youtube/v3/search"


def fetch_videos(query):
    params = {
        "key": API_KEY,
        "part": "snippet",
        "q": query,
        "order": "relevance",  # You can change to "date" for latest videos
        "maxResults": 50,
        "type": "video"
   }
    response = requests.get(API_URL, params=params)
    data = response.json()

    videos = [
        {
            "title": item["snippet"]["title"],
            "videoId": item["id"]["videoId"],
            "channelTitle": item["snippet"]["channelTitle"],
            "embedUrl": f"https://www.youtube.com/embed/{item['id']['videoId']}"
        }
        for item in data.get("items", []) if "videoId" in item["id"]
    ]
    return videos


@app.route('/', methods=['GET'])
def home():
    query = request.args.get('query', 'latest news')  # Default search if empty
    videos = fetch_videos(query)
    return render_template("ht.html", videos=videos, query=query)


if __name__ == '__main__':
    app.run(debug=True)
