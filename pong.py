import os
import subprocess
import threading

path = os.path.dirname(os.path.realpath(__file__))
server_path = os.path.join(path, "server.py")
client_path = os.path.join(path, "client.py")

def launch_client():
    subprocess.call("python " + client_path, creationflags=subprocess.CREATE_NEW_CONSOLE)

def launch_server():
    subprocess.call("python " + server_path, shell = True)


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


client = threading.Thread(target=launch_client)
server = threading.Thread(target=launch_server)

if mode == 1:
    server.start()
    client.start()
elif mode == 2:
    client.start()
elif mode == 3:
    server.start()