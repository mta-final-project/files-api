from fastapi import APIRouter, UploadFile, status, HTTPException
from fastapi.responses import RedirectResponse
from app import service
from app.models import FileMetadata

router = APIRouter()
service = service.S3Service()


# TODO - Check how to use Depends in order not to repeat get_settings() and get_client in each endpoint
@router.get("/download", status_code=status.HTTP_200_OK)
async def download(
    file_name: str,
) -> RedirectResponse:
    if not file_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No file name provided"
        )
    presigned_url = await service.s3_get_presigned_url(file_name)
    return RedirectResponse(url=presigned_url)


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload(file: UploadFile) -> None:
    await service.s3_upload(file)


@router.get("/metadata", status_code=status.HTTP_200_OK)
async def metadata(file_name: str) -> FileMetadata:
    if not file_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No file name provided"
        )
    return await service.s3_get_metadata(file_name)


@router.get("/list-folders", status_code=status.HTTP_200_OK)
async def list_folders(path: str = "") -> list[str]:
    return await service.s3_list_folders(path)


@router.get("/list-objects", status_code=status.HTTP_200_OK)
async def list_objects(path: str = "") -> list[str]:
    return await service.s3_list_objects(path)
