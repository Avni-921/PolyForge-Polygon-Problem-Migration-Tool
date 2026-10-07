import os
from .base import StorageBackend
from .local_backend import LocalStorageBackend
from .azure_backend import AzureStorageBackend
from .s3_backend import S3StorageBackend

def get_storage_backend() -> StorageBackend:
    """
    Factory function to get the appropriate storage backend based on the STORAGE_PROVIDER environment variable.
    """
    provider = os.getenv("STORAGE_PROVIDER", "local").lower()

    if provider == "local":
        return LocalStorageBackend()
    elif provider == "azure":
        return AzureStorageBackend()
    elif provider in ["s3", "r2"]:
        return S3StorageBackend()
    else:
        raise ValueError(f"Unknown STORAGE_PROVIDER: {provider}")
