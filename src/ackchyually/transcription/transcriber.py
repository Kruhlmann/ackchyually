from typing import Optional, Protocol

from ackchyually.youtube.video_id import YouTubeVideoId


class WebVideoTranscriber(Protocol):
    def transcribe_video(self, video_id: YouTubeVideoId) -> Optional[str]:
        pass
