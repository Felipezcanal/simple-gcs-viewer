import datetime

from google.cloud import storage
import os
import shutil
import dotenv

def make_archive(source, destination):
    base = os.path.basename(destination)
    name = base.split('.')[0]
    format = base.split('.')[1]
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))
    shutil.make_archive(name, format, archive_from, archive_to)
    shutil.move('%s.%s' % (name, format), destination)


class Storage:
    def __init__(self):
        dotenv.load_dotenv()
        self.service_account_file = os.environ.get('TRAINING_SERVICE_ACCOUNT_FILE')
        self.project = os.environ.get('TRAINING_SERVICE_ACCOUNT_PROJECT')
        self.bucket_name = os.environ.get('TRAINING_SERVICE_ACCOUNT_BUCKET_NAME')

        self.client = storage.Client.from_service_account_json(self.service_account_file)
        self.bucket = self.client.bucket(self.bucket_name)

    def list_dir(self, gcs_path):
        gcs_path = gcs_path.rstrip('/') + '/'
        if gcs_path == '/':
            gcs_path = ''
        iterator = self.client.list_blobs(self.bucket, prefix=gcs_path, delimiter='/')
        prefixes = []
        for page in iterator.pages:
            for prefix in page.prefixes:
                path = prefix.replace(gcs_path, '')
                path = path.rstrip('/')
                prefixes.append(path)

        objects = []
        for blob in self.client.list_blobs(self.bucket, prefix=gcs_path, delimiter='/'):
            objects.append(blob.name.replace(gcs_path, ''))
        return {
            'prefixes': prefixes,
            'objects': objects
        }

    def get_signed_url(self, url):
        blob = self.bucket.blob(url)
        return {'signed_url': blob.generate_signed_url(
            version="v4",
            # This URL is valid for 15 minutes
            expiration=datetime.timedelta(minutes=15),
            # Allow GET requests using this URL.
            method="GET",
        )}

    def download_files(self, paths):
        for path in paths:
            blob = self.bucket.blob(path)
            local_file = os.path.join('downloads', path)
            local_path = '/'.join(local_file.split('/')[0:-1])
            if not os.path.exists(local_path):
                os.makedirs(local_path)
            blob.download_to_filename(local_file)
        return {'success': True}
