from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.api.deps import SessionDep
from app.services import qrcode_service

router = APIRouter(prefix="/qrcode", tags=["二维码"])


@router.get("/{asset_id}")
def get_qrcode(asset_id: int, db: SessionDep):
    url = qrcode_service.generate_asset_qrcode(db, asset_id)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="设备不存在")
    path = qrcode_service.get_qrcode_path(asset_id)

    return FileResponse(path, media_type="image/png")
