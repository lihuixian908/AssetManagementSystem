import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schemas.common import Response

router = APIRouter(prefix="/upload", tags=["文件上传"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/jpg"}
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "uploads", "photos")


@router.post("", response_model=Response)
async def upload_photo(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, "仅支持 JPG/JPEG/PNG 格式")

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    ext = file.filename.rsplit(".", 1)[-1] if "." in (file.filename or "") else "jpg"
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)

    return Response(data={"url": f"/uploads/photos/{filename}"})
