import os
import subprocess
import threading

from server import start_server
from client import start_client


while True:
    print("Welcome to Net Pong, by vroumm and theel!")
    print()
    print("What do you want to do?")
    print("1. Host and play a game")
    print("2. Connect to a game")
    print("3. Host without playing")
    text  = input("Your choice: ")
    
    try:
        mode = int(text)
    except:
        print("Your choice should be a number")
        continue
    
    if mode < 1 or mode > 3:
        print("Your choice should be between 1 and 3")
        continue
    break

client = threading.Thread(target=start_client)
server = threading.Thread(target=start_server)

if mode == 1:
    server.start()
    client.start()
elif mode == 2:
    client.start()
elif mode == 3:
    server.start()