from ackchyually.transcription.transcriber import WebVideoTranscriber
from ackchyually.youtube.video_id import YouTubeVideoId
from ackchyually.summarizer.transcript import TranscriptSummarizer

class MockTranscriptSummarizer(TranscriptSummarizer):
    def __init__(self, summary: str) -> None:
        self.summary = summary
        
    def summarize_transcript(self, transcript: str) -> str:
        return self.summary

class MockYouTubeVideoId(YouTubeVideoId):
    def __init__(self, id: str) -> None:
        self.id = id
        
    def get_id(self) -> str:
        return self.id

class MockWebVideoTranscriber(WebVideoTranscriber):
    def __init__(self, output: str) -> None:
        self.output = output

    def transcribe_video(self, video_id: YouTubeVideoId) -> str:
        return self.output

def test_summarizer() -> None:
    output = "output"
    video_id = MockYouTubeVideoId("")
    transcriber = MockWebVideoTranscriber(output=output)
    summarizer = MockTranscriptSummarizer("My summary")
    assert transcriber.transcribe_video(video_id=video_id) == output