"""
Storage service for file upload and management
"""
import os
import uuid
from typing import Optional
import boto3
from botocore.exceptions import ClientError
import aiofiles

from ..core.config import settings


class StorageService:
    """Service for cloud storage operations"""

    def __init__(self):
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
        else:
            self.s3_client = None

        self.bucket_name = settings.S3_BUCKET_NAME
        self.local_storage_path = "/tmp/crosspilot_uploads"

    def _generate_file_key(self, user_id: int, filename: str, folder: str = "uploads") -> str:
        """Generate unique file key for storage"""
        ext = os.path.splitext(filename)[1]
        unique_id = str(uuid.uuid4())
        return f"{folder}/{user_id}/{unique_id}{ext}"

    async def upload_file(
        self,
        user_id: int,
        file_content: bytes,
        filename: str,
        content_type: str,
        folder: str = "uploads"
    ) -> str:
        """Upload file to storage and return URL"""
        file_key = self._generate_file_key(user_id, filename, folder)

        if self.s3_client:
            try:
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=file_key,
                    Body=file_content,
                    ContentType=content_type
                )
                return f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{file_key}"
            except ClientError as e:
                raise Exception(f"Failed to upload to S3: {str(e)}")
        else:
            # Local storage fallback
            os.makedirs(os.path.join(self.local_storage_path, folder, str(user_id)), exist_ok=True)
            file_path = os.path.join(self.local_storage_path, file_key)

            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(file_content)

            return f"file://{file_path}"

    async def get_presigned_url(
        self,
        file_key: str,
        expiration: int = 3600
    ) -> Optional[str]:
        """Generate presigned URL for file download"""
        if not self.s3_client:
            return None

        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': file_key},
                ExpiresIn=expiration
            )
            return url
        except ClientError:
            return None

    async def delete_file(self, file_key: str) -> bool:
        """Delete file from storage"""
        if self.s3_client:
            try:
                self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_key)
                return True
            except ClientError:
                return False
        else:
            file_path = os.path.join(self.local_storage_path, file_key)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False


# Create singleton instance
storage_service = StorageService()
