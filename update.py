import site
import sys
import os
import hashlib
import importlib

root_url = "https://api.github.com/repos/DanielRoulin/Games/contents/"
version_url = "https://raw.githubusercontent.com/DanielRoulin/Games/master/VERSION.txt"
requirements_url = "https://raw.githubusercontent.com/DanielRoulin/Games/master/requirements.txt"

path = os.path.dirname(os.path.realpath(__file__))
module_path = os.path.join(path, "pymodules")
version_path = os.path.join(path, "VERSION.txt")


def import_requests():
    sys.path.append(module_path)
    try:
        globals()["requests"] = importlib.import_module("requests")
    except ModuleNotFoundError:
        install_modules("requests")
        importlib.invalidate_caches() 
        importlib.reload(site)
        globals()["requests"] = importlib.import_module("requests")


def install_modules(*modules):
    os.system(f"pip install --target={module_path} {' '.join(modules)}")


def hash_file(path):
    file_size = os.path.getsize(path)
    with open(path, "rb") as f:
        string = f"blob {file_size}\x00".encode() + f.read()
    return hashlib.sha1(string).hexdigest()


def update_available():
    if not os.path.exists(version_path):
        return True
    r = requests.get(version_url)
    remote_version = r.text
    with open(version_path) as f:
        local_version = f.read()
    return remote_version != local_version


def download_files(url):
    files_list = []
    r = requests.get(url)
    files = r.json()
    for f in files:
        if f["type"] == "file": 
            if not f["path"] in (".gitignore", "requirements.txt"):
                complete_path = os.path.join(path, f["path"])
                files_list.append(complete_path)
                if not os.path.exists(complete_path) or f["sha"] != hash_file(complete_path):
                    print("Updating file " + f["path"])
                    r = requests.get(f["download_url"])
                    os.makedirs(os.path.dirname(complete_path), exist_ok=True)
                    with open(complete_path, "wb") as f:
                        f.write(r.content)
        elif f["type"] == "dir":
            files_list.extend(download_files(f["url"]))
    return files_list


def clean(file_list):
    for (root, dirs, files) in os.walk(path, topdown=True):
        for f in files:
            complete_path = os.path.join(root, f)
            if not complete_path in file_list and not "pymodules" in complete_path:
                print("Removing file: " + complete_path)
                os.remove(complete_path)

    for (root, dirs, files) in os.walk(path, topdown=True):
        if not files:
            os.rmdir(root)
    

def check_update():
    import_requests()

    print("Checking for updates...")
    if update_available():
        print("A new update is available!")
        choice = input("Do you want to update? (type 'y' if yes): ")
        if choice == "y":
            print("Installing requirements...")
            r = requests.get(requirements_url)
            install_modules(*r.text.split("\n"))

            print("Updating...")
            files = download_files(root_url)

            print("Cleaning up")
            clean(files)
        else:
            print("Not updating.")
    else:
        print("No updates available")

if __name__ == "__main__":
    check_update()