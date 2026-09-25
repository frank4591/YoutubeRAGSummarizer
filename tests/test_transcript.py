from youtube_app.transcript import extract_video_id, format_transcript


def test_extract_video_id_supports_common_urls():
    assert extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    assert extract_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    assert extract_video_id("https://www.youtube.com/shorts/dQw4w9WgXcQ") == "dQw4w9WgXcQ"


def test_format_transcript_handles_dict_entries():
    result = format_transcript([{"text": "Hello", "start": 1.5}])
    assert result == "Text: Hello Start: 1.5"
