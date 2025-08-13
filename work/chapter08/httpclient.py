#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
from typing import Iterator
import traceback

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
    port = 80
    encoding = 'utf-8'
    request_text = 'GET / HTTP/1.0\r\n\r\n'

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            request_bytes = request_text.encode(encoding)
            send_msg(client_socket, request_bytes)
            received_bytes = b''.join(recv_msg(client_socket))
            received_text = received_bytes.decode(encoding, errors='replace')
            print(received_text)

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

if __name__ == '__main__':
    main()
