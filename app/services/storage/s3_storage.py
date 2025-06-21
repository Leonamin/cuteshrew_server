# s3_adapter.py
import boto3
from app.services.storage.base.base_storage import BaseStorage


class S3Storage(BaseStorage):
    def __init__(self, bucket_name: str):
        self.s3 = boto3.client("s3")
        self.bucket = bucket_name

    def upload(self, file_obj, key, content_type):
        self.s3.upload_fileobj(
            file_obj, self.bucket, key, ExtraArgs={"ContentType": content_type}
        )

    def copy(self, source_key, dest_key):
        self.s3.copy_object(
            Bucket=self.bucket,
            CopySource={"Bucket": self.bucket, "Key": source_key},
            Key=dest_key,
        )

    def delete(self, key):
        self.s3.delete_object(Bucket=self.bucket, Key=key)

    def generate_presigned_url(self, key, content_type, expires_in=60):
        return self.s3.generate_presigned_url(
            "put_object",
            Params={"Bucket": self.bucket, "Key": key, "ContentType": content_type},
            ExpiresIn=expires_in,
        )
