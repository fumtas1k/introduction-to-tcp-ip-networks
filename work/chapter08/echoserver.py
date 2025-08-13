#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
from typing import Iterator

def send_msg(sock: socket.socket, msg: bytes) -> None:
    total_sent_len = 0
    total_msg_len = len(msg)

    while total_sent_len < total_msg_len:
        sent_len = sock.send(msg[total_sent_len:])

        if sent_len == 0:
            raise RuntimeError("socket connection broken")

        total_sent_len += sent_len

def recv_msg(sock: socket.socket, chunk_len: int = 1024) -> Iterator[bytes]:
    while True:
        received_chunk = sock.recv(chunk_len)

        if len(received_chunk) == 0:
            break

        yield received_chunk

def main() -> None:
    host = '127.0.0.1'
    port = 54321

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            server_socket.bind((host, port))
            server_socket.listen()
            print(f"Server listening on {host}:{port}")

            client_socket, (client_address, client_port) = server_socket.accept()
            print(f"Accepted from {client_address}:{client_port}")

            for received_msg in recv_msg(client_socket):
                send_msg(client_socket, received_msg)
                print(f"Echoed: {received_msg}")
            client_socket.close()

    except socket.error as e:
        print(f"Socket error: {e}")
        return

if __name__ == '__main__':
    main()
