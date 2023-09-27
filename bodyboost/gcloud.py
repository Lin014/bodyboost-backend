from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting
from urllib.parse import urljoin

from bodyboost import settings

class GoogleCloudMediaFileStorage(GoogleCloudStorage):
    bucket_name = setting('GS_BUCKET_NAME')
    def url(self, name):
        return urljoin(settings.MEDIA_URL, name)