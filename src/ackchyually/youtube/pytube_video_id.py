from typing import Optional

from pytube import YouTube
from pytube.exceptions import RegexMatchError

from ackchyually.youtube.video_id import YouTubeVideoId


class PyTubeVideoId(YouTubeVideoId):
    def __init__(self, url: str) -> None:
        self.url = url

    def get_id(self) -> Optional[str]:
        try:
            return YouTube(self.url).video_id
        except RegexMatchError:
            return None
