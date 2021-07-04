
import hashlib

def sha1_of_file(file_name):
    sha1 = hashlib.sha1()
    with open(file_name, "rb") as file:
        while True:
            data = file.read(65536)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()
