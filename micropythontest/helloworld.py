#!/usr/bin/env micropython
import sys
import time
import socket
import json
import uselect

# Debug print
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

eprint("Hello, Microworld")

port = 50008
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', port))
sock.setblocking(False)

# USING POLL DOES NOT WORK. Does this need usocket?
# poller = uselect.poll()
# poller.register(sock, uselect.POLLIN)
# res = poller.poll(1000)  # time in milliseconds
# # if not res:
# #     # s is still not ready for input, i.e. operation timed out


for index in range(50):
    time.sleep(0.5)
    eprint("-----" + str(index) + "-----")
    try:
        data = sock.recv(2048).decode('ascii')
        robot_broadcast_data = json.loads(data)
        eprint(robot_broadcast_data)        
    except:
        eprint("no data yet")

sock.close()
   
eprint("Goodbye, Microworld")
