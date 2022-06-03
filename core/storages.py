from django.core.files.storage import FileSystemStorage , Storage 
from django.conf import settings 

class LocalStorage(FileSystemStorage):
  location = settings.LOCAL_MEDIA_ROOT
  base_url = settings.LOCAL_MEDIA_URL

class CloudStorage(Storage):
  location = None 
  base_url = None 

def select_storage()->Storage:
  return LocalStorage() if settings.DEBUG else CloudStorage() 