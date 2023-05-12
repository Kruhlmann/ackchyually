from typing import Protocol

class YouTubeVideoId(Protocol):
    def get_id(self) -> str:
        pass