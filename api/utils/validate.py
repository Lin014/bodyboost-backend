from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
import magic

def validateImage(image):
    allowedFormats = ['image/jpg', 'image/jpeg', 'image/png', 'image/gif']
    fileMimeType = magic.from_buffer(image.read(), mime=True)
    if fileMimeType not in allowedFormats:
        return False
    else:
        return True
    
def validateVideo(video):
    allowedFormats = ['video/mp4', 'video/avi', 'video/mov']
    fileMimeType = magic.from_buffer(video.read(), mime=True)
    if fileMimeType not in allowedFormats:
        return False
    else:
        return True