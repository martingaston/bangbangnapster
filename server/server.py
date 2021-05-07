import socketserver
import threading


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        thread = threading.current_thread()
        print(f"{thread.name} | {self.client_address[0]} wrote:")
        print(self.data)
        self.request.sendall(self.data.upper())


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    server = ThreadedTCPServer(("", 5000), MyTCPHandler)
    with server:
        IP, PORT = server.server_address

        print(f"🚀 Server running on {IP}:{PORT}")

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()
