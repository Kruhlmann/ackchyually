from ackchyually.summarizer.transcript import TranscriptSummarizer


class MockTranscriptSummarizer(TranscriptSummarizer):
    def __init__(self, summary: str) -> None:
        self.summary = summary

    def summarize_transcript(self, transcript: str) -> str:
        return self.summary
