import json
import socket
import time

class Server:
    def __init__(self):
        self.tcp_port = 31313
        self.udp_port = 31314
        
        hostname = socket.gethostname()
        self.ip = socket.gethostbyname(hostname)
        
        # TCP
        self.tcp_sock = socket.socket()
        self.tcp_sock.bind((self.ip, self.tcp_port))
        self.tcp_sock.listen(5)
        self.tcp_sock.setblocking(False)
        
        # UDP for broadcast
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        self.ballx = 40
        self.bally = 10
        self.modx = 1
        self.mody = 1
        
        self.clients = []        
    
    def accept_clients(self):
        try:
            conn, addr = self.tcp_sock.accept()
            print("Got connection from", addr)
            conn.setblocking(False)
            self.clients.append(Client(conn))
        except BlockingIOError:
            pass
        
    def game_logic(self):
        if(self.ballx <= 0):
            self.modx = self.modx * -1
            self.clients[0].score += 1
            self.ballx = 40
            self.bally = 10
            
        if(self.ballx >= 79):
            self.modx = self.modx * -1
            self.clients[1].score += 1
            self.ballx = 40
            self.bally = 10
            
        if(self.bally <= 0 or self.bally >= 25):
            self.mody = self.mody * -1
            
        for c in self.clients:
            if(self.ballx >= 72):
                if(c.paddle_y <= self.bally <= c.paddle_y + 5):
                    self.modx = self.modx * -1
                
            if(self.ballx <= 6):
                if(c.paddle_y <= self.bally <= c.paddle_y + 5):
                    self.modx = self.modx * -1
          
        self.ballx += self.modx
        self.bally += self.mody

    def update(self):
        self.udp_sock.sendto(bytes("", "utf-8"), ("255.255.255.255", self.udp_port))
        
        if len(self.clients) < 2:
            self.accept_clients()
        else:
            self.game_logic()

        for client in self.clients:
            client.update()

class Client:
    def __init__(self, sock):
        self.sock = sock
        self.paddle_x = 0
        self.paddle_y = 0
        self.score = 0
        
        if len(server.clients) == 1:
            self.paddle_x = 3
        else:
            self.paddle_x = 72

    def update(self):
        # Recevied: {"x": 0, "y": 0}
        data = self.recv()
        if data:
            self.paddle_y += data["paddle_y"]

        data = [
            {
                "paddle_x": client.paddle_x,
                "paddle_y": client.paddle_y,
                "ball_x": server.ballx,
                "ball_y": server.bally,
                "score": client.score
            }
        for client in server.clients]
        
        self.send(data)

    def recv(self):
        try:
            data = self.sock.recv(1024)
            if data:
                return json.loads(data.decode("utf-8").split("\n")[0])
        except BlockingIOError:
            pass
        
    def send(self, data):
        self.sock.send(json.dumps(data).encode("utf-8") + b"\n")

def start_server():  
    global server
    server = Server()
    
    print(f"Starting server on {server.ip}")

    while True:
        server.update()
        time.sleep(1/10) 


if __name__ == "__main__":
    start_server()