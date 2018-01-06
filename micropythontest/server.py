#!/usr/bin/env python3
import time
import socket
import json

PORT = 50008
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 0))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:
    data = {'a': 1, 'b': 2}
    message = json.dumps(data).encode('ascii')
    sock.sendto(message, ('<broadcast>', PORT))
    time.sleep(0.1)