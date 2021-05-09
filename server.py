from src.server.server import ThreadedTCPServer, MyTCPHandler

if __name__ == "__main__":
    server = ThreadedTCPServer(("", 5000), MyTCPHandler)
    with server:
        IP, PORT = server.server_address

        print(f"🚀 Server running on {IP}:{PORT}")

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()
