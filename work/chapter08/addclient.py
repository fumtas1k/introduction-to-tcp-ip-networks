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
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")

            operand1, operand2 = 1000, 2000
            print(f"Sending operands: {operand1}, {operand2}")

            request_msg = struct.pack('!ii', operand1, operand2)
            send_msg(client_socket, request_msg)
            print(f"Sent request: {request_msg}")

            received_msg = b''.join(recv_msg(client_socket, 8))
            print(f"Received: {received_msg}")

            (added_value,) = struct.unpack('!q', received_msg)
            print(f"Result: {added_value}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
