# storage_factory.py
from app.services.storage.s3_storage import S3Storage
from app.services.storage.local_storage import LocalStorage  # 구현 예정
from app.services.storage.base.base_storage import BaseStorage
import os


def get_storage() -> BaseStorage:
    storage_type = os.getenv("STORAGE_BACKEND", "s3")

    if storage_type == "s3":
        return S3Storage(bucket_name=os.getenv("S3_BUCKET"))
    elif storage_type == "local":
        return LocalStorage(base_path="./uploads")
    else:
        raise ValueError("Invalid storage backend")
