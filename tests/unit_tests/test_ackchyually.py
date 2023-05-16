from tests.mock.youtube_video_id import MockYouTubeVideoId
from tests.mock.web_video_transcriber import MockWebVideoTranscriber
from tests.mock.transcript_summarizer import MockTranscriptSummarizer

def test_summarizer() -> None:
    output = "output"
    video_id = MockYouTubeVideoId("")
    transcriber = MockWebVideoTranscriber(output=output)
    summarizer = MockTranscriptSummarizer("My summary")
    assert transcriber.transcribe_video(video_id=video_id) == output