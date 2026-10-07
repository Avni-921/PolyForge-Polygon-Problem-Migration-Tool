import os
import boto3
import logging
from botocore.exceptions import ClientError
from .base import StorageBackend

logger = logging.getLogger(__name__)

class S3StorageBackend(StorageBackend):
    def __init__(self):
        self.bucket_name = os.getenv("AWS_STORAGE_BUCKET_NAME")
        if not self.bucket_name:
            raise ValueError("AWS_STORAGE_BUCKET_NAME must be set")

        endpoint_url = os.getenv("AWS_S3_ENDPOINT_URL")
        
        self.s3 = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_S3_REGION_NAME")
        )

    def upload_file(self, key: str, file_obj) -> bool:
        try:
            if hasattr(file_obj, 'read'):
                file_obj.seek(0)
                self.s3.upload_fileobj(file_obj, self.bucket_name, key)
            else:
                self.s3.put_object(Bucket=self.bucket_name, Key=key, Body=file_obj)
            return True
        except ClientError as e:
            logger.error(f"S3 upload failed for {key}: {e}")
            return False

    def download_file(self, key: str) -> bytes:
        response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
        return response['Body'].read()

    def exists(self, key: str) -> bool:
        try:
            self.s3.head_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise

    def list_files(self, prefix: str) -> list[str]:
        paginator = self.s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=self.bucket_name, Prefix=prefix)
        keys = []
        for page in pages:
            for obj in page.get('Contents', []):
                keys.append(obj['Key'])
        return keys

    def delete_file(self, key: str) -> bool:
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError:
            return False
