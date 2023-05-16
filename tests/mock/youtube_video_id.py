from ackchyually.youtube.video_id import YouTubeVideoId


class MockYouTubeVideoId(YouTubeVideoId):
    def __init__(self, id: str) -> None:
        self.id = id

    def get_id(self) -> str:
        return self.id
