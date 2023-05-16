from typing import Optional, Protocol


class YouTubeVideoId(Protocol):
    def get_id(self) -> Optional[str]:
        pass
