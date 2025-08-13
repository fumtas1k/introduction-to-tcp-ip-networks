#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import struct
from typing import Iterator

def send_msg(sock: socket.socket, msg: bytes) -> None:
    total_sent_len = 0
    total_msg_len = len(msg)

    while total_sent_len < total_msg_len:
        sent_len = sock.send(msg[total_sent_len:])

        if sent_len == 0:
            raise RuntimeError("socket connection broken")

        total_sent_len += sent_len

def recv_msg(sock: socket.socket, total_msg_size: int) -> Iterator[bytes]:
    total_recv_size = 0

    while total_recv_size < total_msg_size:
        received_chunk = sock.recv(total_msg_size - total_recv_size)

        if len(received_chunk) == 0:
            raise RuntimeError("socket connection broken")

        yield received_chunk
        total_recv_size += len(received_chunk)

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

            with client_socket:
                received_msg = b''.join(recv_msg(client_socket, 8))
                print(f"Received: {received_msg}")

                (operand1, operand2) = struct.unpack('!ii', received_msg)
                print(f"Operands: {operand1}, {operand2}")

                result = operand1 + operand2
                print(f"Result: {result}")

                result_msg = struct.pack('!q', result)

                send_msg(client_socket, result_msg)
                print(f"Sent result: {result_msg}")

    except socket.error as e:
        print(f"Socket error: {e}")
        return

if __name__ == '__main__':
    main()
