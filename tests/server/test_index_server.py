import pytest


class File:
    def __init__(self, filename, md5, bytes, bitrate, frequency, time):
        self.filename = filename
        self.md5 = md5
        self.bytes = bytes
        self.bitrate = bitrate
        self.frequency = frequency
        self.time = time

    @classmethod
    def from_bytes(cls, byte_input):
        [filename, md5, bytes, bitrate, frequency, time] = byte_input.decode(
            encoding="ascii"
        ).split(" ")

        return cls(
            filename=filename,
            md5=md5,
            bytes=int(bytes),
            bitrate=int(bitrate),
            frequency=int(frequency),
            time=int(time),
        )


@pytest.mark.skip()
def test_can_make_a_file_from_bytes():
    bytes = b'"generic band - generic song.mp3" b92870e0d41bc8e698cf2f0a1ddfeac7-443008 443332 128 44100 60'

    result = File.from_bytes(bytes)

    assert result.filename == "generic band - generic song.mp3"
    assert result.md5 == "b92870e0d41bc8e698cf2f0a1ddfeac7-443008"
    assert result.bytes == 443332
    assert result.bitrate == 128
    assert result.frequency == 44100
    assert result.time == 60
