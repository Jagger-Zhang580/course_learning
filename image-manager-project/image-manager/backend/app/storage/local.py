import os, shutil, uuid
from pathlib import Path
from .base import StorageBackend

class LocalStorage(StorageBackend):
    def __init__(self, base_dir: str = "/app/data/images"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    async def upload(self, file, filename: str) -> dict:
        ext = filename.split(".")[-1] if "." in filename else "jpg"
        key = f"{uuid.uuid4().hex}.{ext}"
        dest = self.base_dir / key
        with open(dest, "wb") as f:
            shutil.copyfileobj(file, f)
        return {"key": key, "url": f"/static/{key}", "size": dest.stat().st_size}

    async def delete(self, object_key: str) -> bool:
        path = self.base_dir / object_key
        if path.exists(): 
            path.unlink()
            return True
        return False

    async def list_files(self, limit=20, offset=0):
        files = sorted(self.base_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
        return [{"key": f.name, "size": f.stat().st_size, "mtime": f.stat().st_mtime} 
                for f in files[offset:offset+limit]]

    def get_url(self, object_key: str) -> str:
        return f"/static/{object_key}"