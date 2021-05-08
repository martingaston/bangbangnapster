from src.payload_parser import parse_payload


class User:
    def __init__(self, nick, password, ip, port, client_info, link_type):
        self.nick = nick
        self.password = password
        self.ip = ip
        self.port = port
        self.client_info = client_info
        self.link_type = link_type

    @classmethod
    def from_bytes_and_ip(cls, bytes_input: bytes, ip):
        parsed = parse_payload(bytes_input)

        [nick, password, port, client_info, link_type] = parsed

        return cls(
            nick=nick,
            password=password,
            ip=ip,
            port=port,
            client_info=client_info,
            link_type=link_type,
        )
