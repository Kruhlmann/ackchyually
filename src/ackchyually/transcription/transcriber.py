from typing import Protocol

from ackchyually.youtube.video_id import YouTubeVideoId

class WebVideoTranscriber(Protocol):
    def transcribe_video(self, video_id: YouTubeVideoId) -> str:
        pass