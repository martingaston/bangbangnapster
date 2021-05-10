import socket

HOST, PORT = "localhost", 50250

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))

    with open("downloads/test2.txt", "ab") as f:
        f.seek(0, 0)
        f.truncate()

        while True:
            received = sock.recv(1024)
            if received == b"":
                break

            f.write(received)
