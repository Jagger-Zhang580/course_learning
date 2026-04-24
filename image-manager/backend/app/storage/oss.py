import oss2, uuid
from .base import StorageBackend

class OSSStorage(StorageBackend):
    def __init__(self, endpoint, bucket_name, access_key, secret_key, cdn_domain=""):
        auth = oss2.Auth(access_key, secret_key)
        self.bucket = oss2.Bucket(auth, endpoint, bucket_name)
        self.cdn_domain = cdn_domain

    async def upload(self, file, filename: str) -> dict:
        ext = filename.split(".")[-1] if "." in filename else "jpg"
        key = f"images/{uuid.uuid4().hex}.{ext}"
        self.bucket.put_object(key, file)
        size = self.bucket.get_object_meta(key).content_length
        return {"key": key, "url": self.get_url(key), "size": size}

    async def delete(self, object_key: str) -> bool:
        self.bucket.delete_object(object_key)
        return True

    async def list_files(self, limit=20, offset=0):
        result = list(oss2.ObjectIterator(self.bucket, max_keys=limit))
        return [{"key": obj.key, "size": obj.size, "mtime": obj.last_modified} for obj in result]

    def get_url(self, object_key: str) -> str:
        if self.cdn_domain:
            return f"https://{self.cdn_domain}/{object_key}"
        return self.bucket.sign_url("GET", object_key, 3600)