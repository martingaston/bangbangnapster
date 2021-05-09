from src.packet_type import PacketType
from src.packet import Packet


def test_can_convert_a_packet_to_bytes():
    packet_length = b"\x1d\x00"  # 29
    packet_type = b"\x02\x00"  # 2
    packet_data = b'foo badpass 6699 "nap v0.8" 3'
    packet = Packet(PacketType.REGISTERED_LOGIN_REQUEST, packet_data.decode("ascii"))

    result = bytes(packet)

    assert result == packet_length + packet_type + packet_data
