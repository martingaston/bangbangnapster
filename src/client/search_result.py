from __future__ import annotations
from dataclasses import dataclass
import ipaddress
from src.link_type import LinkType
from src.payload_parser import parse_payload


@dataclass
class SearchResult:
    filename: str
    md5: str
    size: int
    bitrate: int
    frequency: int
    length: int
    nick: str
    ip: ipaddress.IPv4Address
    link_type: LinkType

    def __repr__(self) -> str:
        return f"{self.filename} (shared by {self.nick})"

    @classmethod
    def from_bytes(cls, bytes_input: bytes) -> SearchResult:
        parsed = parse_payload(bytes_input)

        [filename, md5, size, bitrate, frequency, length, nick, ip, link_type] = parsed

        return cls(
            filename=filename,
            md5=md5,
            size=int(size),
            bitrate=int(bitrate),
            frequency=int(frequency),
            length=int(length),
            nick=nick,
            ip=ipaddress.IPv4Address(int(ip)),
            link_type=LinkType(int(link_type)),
        )
