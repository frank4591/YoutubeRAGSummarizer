"""Production entry point for the YouTube summarizer."""

from youtube_app.config import Settings
from youtube_app.service import YouTubeQAService
from youtube_app.ui import create_demo


def main() -> None:
    settings = Settings.from_env()
    service = YouTubeQAService.from_settings(settings)
    demo = create_demo(service)
    demo.launch(
        server_name=settings.host,
        server_port=settings.port,
        share=settings.share,
    )


if __name__ == "__main__":
    main()
