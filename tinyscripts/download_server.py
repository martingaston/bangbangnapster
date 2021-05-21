import socketserver
import socket
from pathlib import Path
from functools import partial


class PeerServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request: socket.socket
        self.request.sendall(b"1")

        filename = self.request.recv(1024).decode("ascii")
        path = Path.cwd().joinpath("shared", filename)

        if path.exists():
            with path.open(mode="rb") as f:
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


if __name__ == "__main__":
    peer_server()
