from abc import ABC, abstractmethod


class BaseStorage(ABC):
    @abstractmethod
    def upload(self, file_obj, key: str, content_type: str) -> str:
        pass

    @abstractmethod
    def copy(self, source_key: str, dest_key: str) -> None:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass

    @abstractmethod
    def generate_presigned_url(
        self, key: str, content_type: str, expires_in: int = 60
    ) -> str:
        pass
