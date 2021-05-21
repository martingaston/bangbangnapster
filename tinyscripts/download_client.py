import socket
from dataclasses import dataclass
from ipaddress import IPv4Address
from pathlib import Path


use_internet_socket = socket.AF_INET
use_tcp_protocol = socket.SOCK_STREAM


@dataclass
class SearchResult:
    ip: IPv4Address
    port: int
    filename: str


def acknowledge(s: socket.socket) -> bool:
    ack = s.recv(1)
    return ack == b"1"


def download_mp3(result: SearchResult):
    with socket.socket(use_internet_socket, use_tcp_protocol) as s:
        s.connect((str(result.ip), result.port))

        if not acknowledge(s):
            raise ValueError("😔 Not a valid Napster Peer!")

        s.send(result.filename.encode("ascii"))

        file = Path.cwd().joinpath("shared-download", result.filename)
        with file.open(mode="wb") as f:
            while True:
                received = s.recv(1024)
                if received == b"":
                    break

                f.write(received)


if __name__ == "__main__":
    file = SearchResult(ip=IPv4Address("127.0.0.1"), port=6699, filename="test.txt")
    download_mp3(file)
