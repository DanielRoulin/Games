import os
import hashlib


path = "/home/daniel/Downloads/Pong/huscii/__pycache__/renderer.cpython-37.pyc"

def hash_file(path):
    file_size = os.path.getsize(path)
    with open(path, "rb") as f:
        string = f"blob {file_size}\x00".encode() + f.read()
    return hashlib.sha1(string).hexdigest()

print(hash_file(path))