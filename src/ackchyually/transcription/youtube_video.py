from typing import Optional

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled

from ackchyually.transcription.transcriber import WebVideoTranscriber
from ackchyually.youtube.video_id import YouTubeVideoId


class YouTubeVideoTranscriber(WebVideoTranscriber):
    def transcribe_video(self, video_id: YouTubeVideoId) -> Optional[str]:
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id.get_id())
            transcript = ""
            for part in transcript_list:
                transcript += part["text"] + "\n"
            return transcript
        except TranscriptsDisabled:
            return None
        except NoTranscriptFound:
            return None
