from tests.mock.youtube_video_id import MockYouTubeVideoId
from tests.mock.web_video_transcriber import MockWebVideoTranscriber
from tests.mock.transcript_summarizer import MockTranscriptSummarizer

def test_summarizer() -> None:
    transcript = "output"
    video_id = MockYouTubeVideoId("")
    transcriber = MockWebVideoTranscriber(output=transcript)
    summarizer = MockTranscriptSummarizer("My summary")
    assert transcriber.transcribe_video(video_id=video_id) == transcript