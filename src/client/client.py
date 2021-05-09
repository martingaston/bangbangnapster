import socket

HOST, PORT = "localhost", 5000
# HOST, PORT = "ec2-52-56-46-175.eu-west-2.compute.amazonaws.com", 5000
packet_data = b'\x1d\x00\x02\x00foo badpass 6699 "nap v0.8" 3'
mp3_data = b'\x5d\x00\x64\x00"generic band - generic song.mp3" b92870e0d41bc8e698cf2f0a1ddfeac7-443008 443332 128 44100 60'
search_request = b"\x07\x00\xC8\x00generic"
unshare_all = b"\x00\x00\x6E\x00"

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to server and send data
sock.connect((HOST, PORT))
sock.sendall(packet_data)

# Receive data from the server and shut down
received = str(sock.recv(1024), "ascii")

sock.sendall(mp3_data)

sock.sendall(search_request)

packet_length = sock.recv(2)
packet_type = int.from_bytes(sock.recv(2), byteorder="little")
packet_data = sock.recv(int.from_bytes(packet_length, byteorder="little"))

print(packet_data.decode("ascii"))

packet_length = sock.recv(2)
packet_type = int.from_bytes(sock.recv(2), byteorder="little")
packet_data = sock.recv(int.from_bytes(packet_length, byteorder="little"))

print(packet_data.decode("ascii"))

sock.sendall(unshare_all)
sock.close()

print("Sent:     {}".format(packet_data))
print("Received: {}".format(received))
