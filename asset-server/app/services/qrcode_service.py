import os
import qrcode
from sqlalchemy.orm import Session

from app.models.asset import Asset

QR_BASE_URL = os.getenv("QR_BASE_URL", "http://localhost:3000")
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "qrcode")


def _ensure_dir():
    os.makedirs(UPLOAD_DIR, exist_ok=True)


def generate_asset_qrcode(db: Session, asset_id: int) -> str | None:
    asset = db.get(Asset, asset_id)
    if not asset:
        return None

    _ensure_dir()

    content = f"{QR_BASE_URL}/scan/result/{asset.asset_code}"
    filename = f"asset_{asset_id}.png"
    filepath = os.path.join(UPLOAD_DIR, filename)
    url = f"/uploads/qrcode/{filename}"

    img = qrcode.make(content)
    img.save(filepath)

    asset.qr_code_url = url
    db.add(asset)
    db.commit()

    return url


def get_qrcode_path(asset_id: int) -> str | None:
    _ensure_dir()
    filename = f"asset_{asset_id}.png"
    filepath = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(filepath):
        return filepath
    return None
