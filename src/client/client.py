import socket

from src.packet import Packet, read_packet
from src.packet_type import PacketType
from typing import Optional

# HOST, PORT = "ec2-52-56-46-175.eu-west-2.compute.amazonaws.com", 5000
packet_data = b'\x1d\x00\x02\x00foo badpass 6699 "nap v0.8" 3'
mp3_data = b'\x5d\x00\x64\x00"generic band - generic song.mp3" b92870e0d41bc8e698cf2f0a1ddfeac7-443008 443332 128 44100 60'
search_request = b"\x07\x00\xC8\x00generic"
unshare_all = b"\x00\x00\x6E\x00"


class Client:
    host: str
    port: int

    def __init__(self, host: str = "localhost", port: int = 5000):
        self.host = host
        self.port = port

    def start(self):
        # Create a socket (SOCK_STREAM means a TCP socket)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            print("!!napster")

            # login
            sock.sendall(packet_data)
            logged_in = read_packet(sock)
            if logged_in.packet_type != PacketType.LOGIN_ACKNOWLEDGE:
                print("failed to login, exiting")
                exit(1)

            # share all files
            sock.sendall(mp3_data)

            # start a search request
            sock.sendall(search_request)

            while True:
                packet = read_packet(sock)
                if packet is None:
                    break

                response = self.handle_packet(packet)
                if response is not None:
                    sock.sendall(bytes(response))

            # logout
            sock.sendall(unshare_all)

    def handle_packet(self, packet: Packet) -> Optional[Packet]:
        if packet.packet_type == PacketType.SEARCH_QUERY_RESULTS:
            print(packet)
            return None

        if packet.packet_type == PacketType.SEARCH_QUERY_RESULTS_END_NOTIFICATION:
            print("end of search results")
            return None

        return None
