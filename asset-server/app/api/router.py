from fastapi import APIRouter

from app.api.v1 import auth, users, assets, categories, reports, borrow, change, qrcode, upload

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(reports.router)
api_router.include_router(assets.router)
api_router.include_router(categories.router)
api_router.include_router(borrow.router)
api_router.include_router(change.router)
api_router.include_router(qrcode.router)
api_router.include_router(upload.router)

router = APIRouter(prefix="/api/v1")
router.include_router(api_router)