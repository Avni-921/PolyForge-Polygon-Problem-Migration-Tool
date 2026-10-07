import os
import logging
from azure.storage.blob import BlobServiceClient
from .base import StorageBackend

logger = logging.getLogger(__name__)

class AzureStorageBackend(StorageBackend):
    def __init__(self):
        conn_str = os.getenv("AZURE_CONNECTION_STRING")
        container = os.getenv("AZURE_CONTAINER_NAME")
        if not conn_str or not container:
            raise ValueError("AZURE_CONNECTION_STRING and AZURE_CONTAINER_NAME must be set")
        
        self.blob_service_client = BlobServiceClient.from_connection_string(conn_str)
        self.container_name = container
        self.container_client = self.blob_service_client.get_container_client(container)
        
        # Ensure container exists
        if not self.container_client.exists():
            self.container_client.create_container()

    def upload_file(self, key: str, file_obj) -> bool:
        try:
            blob_client = self.container_client.get_blob_client(key)
            if hasattr(file_obj, 'read'):
                file_obj.seek(0)
                blob_client.upload_blob(file_obj, overwrite=True)
            else:
                blob_client.upload_blob(file_obj, overwrite=True)
            return True
        except Exception as e:
            logger.error(f"Azure upload failed for {key}: {e}")
            return False

    def download_file(self, key: str) -> bytes:
        blob_client = self.container_client.get_blob_client(key)
        return blob_client.download_blob().readall()

    def exists(self, key: str) -> bool:
        blob_client = self.container_client.get_blob_client(key)
        return blob_client.exists()

    def list_files(self, prefix: str) -> list[str]:
        blobs = self.container_client.list_blobs(name_starts_with=prefix)
        return [blob.name for blob in blobs]

    def delete_file(self, key: str) -> bool:
        blob_client = self.container_client.get_blob_client(key)
        if blob_client.exists():
            blob_client.delete_blob()
            return True
        return False
