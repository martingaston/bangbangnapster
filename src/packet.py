from dataclasses import dataclass
import struct
from src.packet_type import PacketType


@dataclass
class Packet:
    packet_length: int
    packet_type: PacketType
    data: bytes

    def __init__(self, packet_type: PacketType, data: str):
        self.packet_type = packet_type
        self.data = data.encode("ascii", errors="replace")
        self.packet_length = len(self.data)

    def __bytes__(self) -> bytes:
        return (
            _int_to_napster_bytes(self.packet_length)
            + _int_to_napster_bytes(self.packet_type.value)
            + self.data
        )


def _int_to_napster_bytes(num: int) -> bytes:
    LITTLE_ENDIAN_UNSIGNED_SHORT = "<H"
    return struct.pack(LITTLE_ENDIAN_UNSIGNED_SHORT, num)
