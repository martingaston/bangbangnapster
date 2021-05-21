import socketserver
import socket


class NapsterServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class NapsterHandler(socketserver.BaseRequestHandler):
    def handle(self):
        s: socket.socket = self.request

        i_have_no_idea_how_many_bytes_to_read_right_now = 1024
        req = s.recv(i_have_no_idea_how_many_bytes_to_read_right_now)

        # TODO: do a napster here

        response_packet = b"\x17\x00\x03\x00mycoolemail@hotmail.com"
        s.sendall(response_packet)


server = NapsterServer(("", 7777), NapsterHandler)
with server:
    IP, PORT = server.server_address

    print(f"🚀 Server running on {IP}:{PORT}")
    server.serve_forever()
