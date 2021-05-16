import ipaddress
from src.link_type import LinkType
from src.payload_parser import parse_payload


class User:
    def __init__(self, nick, password, ip, port, client_info, link_type):
        self.nick: str = nick
        self.password: str = password
        self.ip: int = ip
        self.port: int = port
        self.client_info: str = client_info
        self.link_type: LinkType = link_type

    @classmethod
    def from_bytes_and_ip(cls, bytes_input: bytes, ip: str):
        parsed = parse_payload(bytes_input)

        [nick, password, port, client_info, link_type] = parsed

        return cls(
            nick=nick,
            password=password,
            ip=int(ipaddress.IPv4Address(ip)),
            port=int(port),
            client_info=client_info,
            link_type=LinkType(int(link_type)),
        )
