import requests
import os
import hashlib

root_url = "https://api.github.com/repos/DanielRoulin/Games/contents/"
version_url = "https://raw.githubusercontent.com/DanielRoulin/Games/master/VERSION.txt"

path = os.path.dirname(os.path.realpath(__file__))
version_path = os.path.join(path, "VERSION.txt")

def hash_file(path):
    file_size = os.path.getsize(path)
    with open(path) as f:
        string = f"blob {file_size}\x00{f.read()}"
    return hashlib.sha1(string.encode()).hexdigest()

def update_available():
    if not os.path.exists(version_path):
        return True

    r = requests.get(version_url)
    remote_version = r.text
    with open(version_path) as f:
        local_version = f.read()
    return remote_version != local_version


def download_files(url):
    r = requests.get(url)
    files = r.json()
    for f in files:
        if f["type"] == "file":
            complete_path = os.path.join(path, f["path"])
            if not os.path.exists(complete_path) or f["sha"] != hash_file(complete_path):
                r = requests.get(f["download_url"])
                os.makedirs(os.path.dirname(complete_path), exist_ok=True)
                with open(complete_path, "wb") as f:
                    f.write(r.content)
        elif f["type"] == "dir":
            download_files(f["url"])

if __name__ == "__main__":
    if update_available():
        download_files(root_url)