import socket
import socketserver
import struct

from src.client.name_generator import generate_username
from src.packet import Packet, read_packet
from src.packet_type import PacketType
from src.client.search_result import SearchResult
from pathlib import Path
from typing import Optional
import threading
from functools import partial
from hashlib import md5

# HOST, PORT = "ec2-52-56-46-175.eu-west-2.compute.amazonaws.com", 5000


class PeerServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request: socket.socket
        self.request.sendall(b"1")
        filename = self.request.recv(1024).decode("ascii")
        path = Path("shared").joinpath(filename)

        if path.exists():
            with open(path, "rb") as f:
                for chunk in iter(partial(f.read, 1024), b""):
                    self.request.sendall(chunk)


class PeerTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def peer_server(port=6699):
    server = PeerTCPServer(("", port), PeerServerHandler)
    with server:
        IP, PORT = server.server_address
        print(f"🤝 Peer server active on {IP}:{PORT}")

        server.serve_forever()


class Client:
    host: str
    port: int

    def __init__(self, host: str = "localhost", port: int = 5000):
        self.host = host
        self.port = port

    def start(self):

        x = threading.Thread(target=peer_server, daemon=True)
        x.start()
        # Create a socket (SOCK_STREAM means a TCP socket)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            self.sock = sock
            sock.connect((self.host, self.port))

            motd = Path.cwd().joinpath("src", "client", "motd").read_text()
            print(motd)

            # login
            self._login()
            self._share_all_files()

            self._main_menu()

    def _login(self):
        data = f'{generate_username()} nopass 6699 "bangbangnapster 0.1" 3'
        packet = Packet(PacketType.REGISTERED_LOGIN_REQUEST, data)
        self.sock.sendall(bytes(packet))
        logged_in = read_packet(self.sock)
        if logged_in.packet_type != PacketType.LOGIN_ACKNOWLEDGE:
            print("failed to login, exiting")
            exit(1)

    def _logout(self):
        unshare_all = b"\x00\x00\x6E\x00"
        self.sock.sendall(unshare_all)
        exit(0)

    def _share_all_files(self):
        library = Path.cwd().joinpath("shared").glob("*.mp3")

        for mp3 in library:
            mp3_bytes = mp3.read_bytes()
            hash = md5(mp3_bytes).hexdigest()
            packet = Packet(
                PacketType.ADD_A_FILE_TO_SHARED_FILE_INDEX,
                f'"{mp3.name}" {hash} {len(mp3_bytes)} 128 44100 60',
            )
            self.sock.sendall(bytes(packet))

    def _main_menu(self):
        print("Select an option:")
        print("1. Search for a file")
        print("2. Log out")

        selection = input(">>> ")

        if selection == "1":
            self._search_for_files()
        elif selection == "2":
            self._logout()

    def _search_for_files(self):
        print("What shall we search for?")
        selection = input(">>> ")

        search_request = (
            struct.pack("<H", len(selection))
            + b"\xC8\x00"
            + bytes(selection, encoding="ascii")
        )

        self.sock.sendall(search_request)

        self._get_search_results()

    def _get_search_results(self):
        results = []

        while True:
            packet = read_packet(self.sock)
            if packet.packet_type is PacketType.SEARCH_QUERY_RESULTS:
                results.append(SearchResult.from_bytes(packet.data))

            elif packet.packet_type is PacketType.SEARCH_QUERY_RESULTS_END_NOTIFICATION:
                break

            else:
                print("Server returned unexpected response. Whoops! Exiting.")
                self._logout()

        self._show_download_options(results)

    def _show_download_options(self, results):
        MAX_RESULTS = 5
        print("results:")
        for index, result in enumerate(results[:MAX_RESULTS]):
            print(f"{index}. {result}")
        print("5. Return to main menu")

        print("would you like to download any of these files?")
        res = input(">>> ")

        if res == "0" or res == "1" or res == "2" or res == "3" or res == "4":
            self._download(results[int(res)])

        if res == "5":
            self._main_menu()

    def _download(self, result: SearchResult):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((str(result.ip), 6699))
            ack = sock.recv(1)
            if ack.decode("ascii") == "1":
                print(
                    f"☎️  connected to {result.ip}, attempting to download {result.filename}"
                )

            sock.send(bytes(result.filename.encode("ascii")))

            with open(f"shared/{result.filename}", "wb") as f:
                while True:
                    received = sock.recv(1024)
                    if received == b"":
                        break

                    f.write(received)

        print(
            f"🎉  download of {result.filename} from {result.nick} ({result.size} bytes) complete"
        )

        self._main_menu()

    def _handle_packet(self, packet: Packet) -> Optional[Packet]:
        if packet.packet_type == PacketType.SEARCH_QUERY_RESULTS:
            print(packet)
            return None

        if packet.packet_type == PacketType.SEARCH_QUERY_RESULTS_END_NOTIFICATION:
            print("end of search results")
            return None

        return None
