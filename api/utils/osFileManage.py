import os

def deleteFile(file):
    if (file.path != ''):
        if (os.path.exists(file.path)):
            os.remove(file.path)