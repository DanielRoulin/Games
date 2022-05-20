import socket
import time
import json

import os
import sys
module_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pymodules")
sys.path.append(module_path)

import keyboard  
from huscii.renderer import HUSCIIRenderer


class Client:
    def __init__(self):
        self.tcp_port = 31313
        self.udp_port = 31314
        
        self.find_server()
        
        self.tcp_sock = socket.socket()
        self.tcp_sock.connect((self.ip, self.tcp_port))
        self.tcp_sock.setblocking(False)
        
    def find_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("0.0.0.0", self.udp_port))
        
        # Waiting for connection...
        data, addr = sock.recvfrom(1024)
        self.ip = addr[0]
        
    def send(self, data):
        data = json.dumps(data).encode("utf-8") + b"\n"
        self.tcp_sock.send(data)

    def recv(self):
        try:
            data = self.tcp_sock.recv(1024)
            return json.loads(data.decode("utf-8").split("\n")[0])
        except BlockingIOError:
            pass

def start_client():
    local_client = Client()
    renderer = HUSCIIRenderer()
    while True:
        # Sending
        data = {"paddle_y": 0}
        if keyboard.is_pressed("w"):
            data["paddle_y"] -= 1
        if keyboard.is_pressed("s"):
            data["paddle_y"] += 1

        local_client.send(data)


        # Receiving
        data = local_client.recv()
        if data:
            print("Player 1 score: " + data[0]["score"] + "             Player 2 score: " + data[1]["score"])
            for client in data:
                x, y = client["paddle_x"], client["paddle_y"]
                bx, by = client["ball_x"], client["ball_y"]
                score = client["score"]
                renderer.rect(x, y, 3, 5)
                renderer.rect(bx, by, 2, 2)
        
        # Drawing
        renderer.draw()
        time.sleep(1/10)


if __name__ == "__main__":
    start_client()