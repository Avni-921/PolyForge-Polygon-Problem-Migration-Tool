import os
import shutil
from .base import StorageBackend

class LocalStorageBackend(StorageBackend):
    def __init__(self, base_dir="local_storage"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def _get_path(self, key: str) -> str:
        return os.path.join(self.base_dir, key)

    def upload_file(self, key: str, file_obj) -> bool:
        path = self._get_path(key)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # Handle both string/bytes content and file objects
        if hasattr(file_obj, 'read'):
            content = file_obj.read()
            if isinstance(content, str):
                content = content.encode('utf-8')
            with open(path, 'wb') as f:
                f.write(content)
        else:
            with open(path, 'wb') as f:
                if isinstance(file_obj, str):
                    f.write(file_obj.encode('utf-8'))
                else:
                    f.write(file_obj)
        return True

    def download_file(self, key: str) -> bytes:
        path = self._get_path(key)
        if not os.path.exists(path):
            raise FileNotFoundError(f"File {key} not found.")
        with open(path, 'rb') as f:
            return f.read()

    def exists(self, key: str) -> bool:
        return os.path.exists(self._get_path(key))

    def list_files(self, prefix: str) -> list[str]:
        keys = []
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, self.base_dir).replace('\\', '/')
                if rel_path.startswith(prefix):
                    keys.append(rel_path)
        return keys

    def delete_file(self, key: str) -> bool:
        path = self._get_path(key)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False
