from django.db import connection
from django.conf import settings
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import quote



def execute_query(query, params=None, fetchone=False, fetchall=False):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if fetchone:
            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row)) if row else None 
        if fetchall:
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        connection.commit()


class BunnyCDNStorage:
    def __init__(self):
        self.api_key = settings.BUNNY_CDN_ACCESS_KEY
        self.storage_zone = settings.BUNNY_CDN_STORAGE_ZONE_NAME
        self.pull_zone = settings.BUNNY_CDN_PULL_ZONE
        self.base_url = settings.BUNNY_CDN_BASE_URL
        self.headers = {
            'AccessKey': self.api_key,
            'Content-Type': 'application/octet-stream',
            'Accept': 'application/json'
        }

    def create_session_with_retries(self):
        session = requests.Session()
        retry_strategy = Retry(
            total=5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def upload_file(self, storage_path, file_content, file_name):
        try:
            # Create a session with retry strategy
            session = self.create_session_with_retries()

            # Construct the full storage URL
            storage_url = f'{self.base_url}{storage_path}/{file_name}'
            response = session.put(storage_url, data=file_content, headers=self.headers)
            response.raise_for_status()

            # Construct the CDN URL to access the uploaded file
            cdn_url = f'https://{self.pull_zone}.b-cdn.net/{storage_path}/{file_name}'
            return cdn_url
        except Exception as error:
            raise Exception(f"Failed to upload video: {error}")
        
    
    def delete_object(self, file_path):
        """
        Deletes an object (file) from BunnyCDN at the specified file path.
        """
        try:
            session = self.create_session_with_retries()
            url = f"{self.base_url}{file_path}"
            response = session.delete(url, headers=self.headers)
            response.raise_for_status()
            return True
        except Exception as error:
            raise Exception(f"Failed to delete object: {error}")