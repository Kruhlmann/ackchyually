from ackchyually.youtube.video_id import YouTubeVideoId

from pytube import YouTube

class PyTubeVideoId(YouTubeVideoId):
    def __init__(self, url: str) -> None:
        self.url = url

    def get_id(self) -> str:
        return YouTube(self.url).video_id