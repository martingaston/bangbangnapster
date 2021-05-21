import socket

use_internet_socket = socket.AF_INET
use_tcp_protocol = socket.SOCK_STREAM

with socket.socket(use_internet_socket, use_tcp_protocol) as s:
    host = 'bangbangcon.com'
    port = 80

    s.connect((host, port))
    s.sendall(b"GET / HTTP/1.1\r\n")
    s.sendall(b"Host: bangbangcon.com\r\n")
    s.sendall(b"Connection: close\r\n")
    s.sendall(b"\r\n")

    response = s.recv(2048)

print("✨ i travelled across the internet to get you this 👇 ✨")
print(response.decode("ascii"))
