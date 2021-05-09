from src.payload_parser import parse_payload


class File:
    def __init__(self, filename, md5, size_in_bytes, bitrate, frequency, time):
        self.filename: str = filename
        self.md5: str = md5
        self.size_in_bytes: int = size_in_bytes
        self.bitrate: int = bitrate
        self.frequency: int = frequency
        self.time: int = time

    @classmethod
    def from_bytes(cls, byte_input: bytes):
        parsed = parse_payload(byte_input)

        [filename, md5, size_in_bytes, bitrate, frequency, time] = parsed

        return cls(
            filename=filename,
            md5=md5,
            size_in_bytes=int(size_in_bytes),
            bitrate=int(bitrate),
            frequency=int(frequency),
            time=int(time),
        )
