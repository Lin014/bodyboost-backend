import os

def deleteFile(file):
    if file:
        if (os.path.exists(file.path)):
            os.remove(file.path)