import socket

use_internet_socket = socket.AF_INET
use_tcp_protocol = socket.SOCK_STREAM

napster_server_host = "www.mycoolnapsterserver.com"
napster_server_port = 7777

napster_data_packet = b'\x1d\x00\x02\x00username password 6699 "mycoolnapster 0.1" 3'

with socket.socket(use_internet_socket, use_tcp_protocol) as s:
    s.connect((napster_server_host, napster_server_port))
    s.sendall(napster_data_packet)

    i_have_no_idea_how_many_bytes_to_read_right_now = 1024
    s.recv(i_have_no_idea_how_many_bytes_to_read_right_now)
