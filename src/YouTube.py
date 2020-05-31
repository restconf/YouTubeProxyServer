import json
import pytube_fork

class YouTube:

    def __init__(self, response:str):
        self.jsonObj = json.loads(response)
        for item in self.jsonObj["items"]:
            if "channelId" in item["id"]:
                del self.jsonObj["items"][0]

    def get_Thumbnail(self):
        thumbnail_urls = []
        for item in self.jsonObj["items"]:
            thumbnail_urls.append(item["snippet"]["thumbnails"]["high"]["url"])
        return thumbnail_urls

    def get_ids(self):
        video_ids = []
        for item in self.jsonObj["items"]:
            video_ids.append(item["id"]["videoId"])
        direct_urls = []
        for id in video_ids:
            direct_urls.append(pytube_fork.YouTube(f"https://www.youtube.com/watch?v={id}").streams.get_by_itag(18).url)
        return direct_urls