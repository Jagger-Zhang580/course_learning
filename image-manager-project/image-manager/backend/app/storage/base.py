from abc import ABC, abstractmethod
from typing import BinaryIO

class StorageBackend(ABC):
    @abstractmethod
    async def upload(self, file: BinaryIO, filename: str) -> dict:
        pass
    @abstractmethod
    async def delete(self, object_key: str) -> bool:
        pass
    @abstractmethod
    async def list_files(self, limit: int = 20, offset: int = 0) -> list:
        pass
    @abstractmethod
    def get_url(self, object_key: str) -> str:
        pass