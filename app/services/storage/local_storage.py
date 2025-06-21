import os
from pathlib import Path
from app.services.storage.base.base_storage import BaseStorage


class LocalStorage(BaseStorage):
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        os.makedirs(self.base_path, exist_ok=True)

    def upload(self, file_obj, key: str, content_type: str) -> str:
        file_path = self.base_path / key
        os.makedirs(file_path.parent, exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(file_obj.read())
        return str(file_path)

    def copy(self, source_key: str, dest_key: str) -> None:
        source_path = self.base_path / source_key
        dest_path = self.base_path / dest_key

        os.makedirs(dest_path.parent, exist_ok=True)
        with open(source_path, "rb") as src, open(dest_path, "wb") as dst:
            dst.write(src.read())

    def delete(self, key: str) -> None:
        file_path = self.base_path / key
        if file_path.exists():
            os.remove(file_path)

    def generate_presigned_url(
        self, key: str, content_type: str, expires_in: int = 60
    ) -> str:
        # Local storage doesn't need presigned URLs, just return the local file path
        return str(self.base_path / key)
