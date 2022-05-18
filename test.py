import os
import hashlib


path = ""

def hash_file(path):
    file_size = os.path.getsize(path)
    with open("VERSION.txt") as f:
        string = f"blob {file_size}\x00{f.read()}"
    return hashlib.sha1(string.encode()).hexdigest()

def a():
    print("A")

if not True and a():
    print("B")

# file exists, sha same
# file exists, sha not same => d
# file not exists =>

complete_path = os.path.join(path, "VERSION.txt")
if not os.path.exists(complete_path) or "56a6051ca2b02b04ef92d5150c9ef600403cb1de" != hash_file(complete_path):
    print("download")