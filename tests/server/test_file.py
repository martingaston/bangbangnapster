from src.server.file import File


def test_can_make_a_file_from_bytes():
    bytes = b'"generic band - generic song.mp3" b92870e0d41bc8e698cf2f0a1ddfeac7-443008 443332 128 44100 60'

    result = File.from_bytes(bytes)

    assert result.filename == "generic band - generic song.mp3"
    assert result.md5 == "b92870e0d41bc8e698cf2f0a1ddfeac7-443008"
    assert result.size_in_bytes == 443332
    assert result.bitrate == 128
    assert result.frequency == 44100
    assert result.time == 60
