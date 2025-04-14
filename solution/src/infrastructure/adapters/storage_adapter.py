from typing import Protocol, Self

import boto3
from dishka import Provider, Scope, provide

from src.core.settings import Settings


class StorageAdapterProtocol(Protocol):
    async def upload_file(self: Self, filename: str, data: bytes) -> str: ...

    async def get_file(self: Self, filename: str) -> bytes | None: ...

    async def delete_file(self: Self, filename: str) -> bool: ...


class StorageAdapterImpl:
    def __init__(self, settings: Settings, bucket_name: str = "main"):
        self.url = "http://minio:9000"
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=self.url,
            aws_access_key_id=settings.minio.user,
            aws_secret_access_key=settings.minio.password,
        )

        self.bucket_name = bucket_name
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except:
            self.s3_client.create_bucket(Bucket=self.bucket_name)

    async def upload_file(self, filename: str, data: bytes) -> str:
        self.s3_client.put_object(Bucket=self.bucket_name, Key=filename, Body=data)
        return f"{self.url}/{self.bucket_name}/{filename}"

    async def get_file(self, filename: str) -> bytes | None:
        try:
            file_obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=filename)
            return file_obj["Body"].read()
        except self.s3_client.exceptions.NoSuchKey:
            return None

    async def delete_file(self, filename: str) -> bool:
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=filename)
            return True
        except Exception:
            return False


class StorageAdapterProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_dependency(self, settings: Settings) -> StorageAdapterProtocol:
        return StorageAdapterImpl(settings)
