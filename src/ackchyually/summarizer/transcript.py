from typing import Protocol

class TranscriptSummarizer(Protocol):
    def summarize_transcript(self, transcript: str) -> str:
        pass