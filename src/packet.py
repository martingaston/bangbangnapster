from dataclasses import dataclass
import struct
from src.packet_type import PacketType
from typing import Optional


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


def read_packet(socket) -> Optional[Packet]:
    packet_length = socket.recv(2)
    packet_type = int.from_bytes(socket.recv(2), byteorder="little")
    packet_data = socket.recv(int.from_bytes(packet_length, byteorder="little"))

    if packet_length == b"" and packet_type == 0 and packet_data == b"":
        return None

    return Packet(PacketType(packet_type), packet_data.decode("ascii"))
