import boto3
from fastapi import File, HTTPException, status
from app.settings import get_settings
from botocore.exceptions import ClientError
from app.models import FileMetadata, FileInfo
from botocore import UNSIGNED
from botocore.client import Config


class S3Service:
    def __init__(self):
        self.settings = get_settings()
        self.s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))

    def is_file_exists(self, file_name: str) -> bool:
        try:
            self.s3_client.head_object(
                Bucket=self.settings.aws_bucket_name, Key=file_name
            )
        except ClientError as error:
            if error.response["Error"]["Message"] == "Not Found":
                return False
            raise error
        return True

    async def s3_get_metadata(self, file_name: str) -> FileMetadata:
        if not self.is_file_exists(file_name):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
            )
        http_headers = self.s3_client.head_object(
            Bucket=self.settings.aws_bucket_name, Key=file_name
        )["ResponseMetadata"]["HTTPHeaders"]
        return FileMetadata.from_http_headers(file_name, http_headers)

    async def s3_get_presigned_url(self, file_name: str) -> str:
        if not self.is_file_exists(file_name):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
            )

        return self.s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.settings.aws_bucket_name, "Key": file_name},
            ExpiresIn=self.settings.presigned_url_expiration,
        )

    async def s3_upload(self, file: File) -> None:
        file_name = file.filename
        self.s3_client.upload_fileobj(
            file.file, self.settings.aws_bucket_name, file_name
        )

    async def s3_list_folders(self, path: str) -> list[str]:
        if path:
            path = path + "/"
        response = self.s3_client.list_objects_v2(
            Bucket=self.settings.aws_bucket_name, Delimiter="/", Prefix=path
        )
        subfolders = [file["Prefix"][:-1] for file in response.get("CommonPrefixes", [])]
        return subfolders

    async def s3_list_objects(self, path: str) -> list[FileInfo]:
        response = self.s3_client.list_objects_v2(
            Bucket=self.settings.aws_bucket_name, Prefix=path
        )
        contents = response.get("Contents", [])
        files_info = [FileInfo.from_contents(content) for content in contents]
        return files_info
