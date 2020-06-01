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
        for index, item in enumerate(self.jsonObj["items"]):
            video_ids.append(item["id"]["videoId"])
        return video_ids

