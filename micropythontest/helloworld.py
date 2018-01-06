#!/usr/bin/env micropython
import sys
import time
import socket
import json

# Debug print
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

eprint("Hello, Microworld")

port = 50008
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', port))
sock.setblocking(False)

for index in range(50):
    time.sleep(0.5)
    eprint("-----" + str(index) +"-----")

    # Should be using uselect.poll instead of try/except, but that doesn't work yet.
    # See "Instead of ... use ..." at http://docs.micropython.org/en/latest/wipy/library/usocket.html#usocket.socket.settimeout

    try:
        data = sock.recv(2048).decode('ascii')
        robot_broadcast_data = json.loads(data)
        eprint(robot_broadcast_data)        
    except:
        eprint("no data yet")

sock.close()
   
eprint("Goodbye, Microworld")
