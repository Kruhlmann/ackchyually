from ackchyually.transcription.transcriber import WebVideoTranscriber
from ackchyually.youtube.video_id import YouTubeVideoId


class MockWebVideoTranscriber(WebVideoTranscriber):
    def __init__(self, output: str) -> None:
        self.output = output

    def transcribe_video(self, video_id: YouTubeVideoId) -> str:
        return self.output
