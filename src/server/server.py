import socketserver
import threading
from src.server.index_server import IndexServer
from src.server.user import User
from src.server.file import File
from src.packet import Packet, read_packet
from src.packet_type import PacketType


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            packet = read_packet(self.request)
            if packet is None:
                break

            thread = threading.current_thread()
            print(f"{thread.name} | {self.client_address[0]} wrote:")
            print(packet)

            response = self._handle_packet(packet)

            if response is not None:
                self.request.sendall(bytes(response))

    def _handle_packet(self, packet: Packet) -> Packet:
        if packet.packet_type == PacketType.REGISTERED_LOGIN_REQUEST:
            self.user = User.from_bytes_and_ip(packet.data, self.client_address[0])
            return Packet(PacketType.LOGIN_ACKNOWLEDGE, "noemailstored@here.com")

        if packet.packet_type == PacketType.ADD_A_FILE_TO_SHARED_FILE_INDEX:
            index_server = IndexServer()
            file = File.from_bytes(packet.data)
            index_server.add(file, self.user)
            return None

        if (
            packet.packet_type
            == PacketType.UNSHARE_ALL_FILES_FROM_THE_SHARED_FILE_INDEX
        ):
            index_server = IndexServer()
            removed = index_server.remove_all(self.user)
            return Packet(
                PacketType.UNSHARE_ALL_FILES_FROM_THE_SHARED_FILE_INDEX, str(removed)
            )

        if packet.packet_type == PacketType.SEARCH_QUERY_REQUEST:
            index_server = IndexServer()
            results = index_server.search("generic song")
            for result in results:
                packet = Packet(PacketType.SEARCH_QUERY_RESULTS, str(result))
                self.request.sendall(bytes(packet))

            return Packet(PacketType.SEARCH_QUERY_RESULTS_END_NOTIFICATION, "")

        return Packet(PacketType.LOGOUT_OR_ERROR_MESSAGE_FROM_SERVER, "error")


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
