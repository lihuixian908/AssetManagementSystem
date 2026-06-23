import os

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
import logging

from app.api.router import router
from app.db.base import Base
from app.db.session import engine
from app.models import User, Category, Asset, AssetRecord, AssetBorrowRecord, AssetChangeRecord  # noqa: F401

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title="固定资产管理系统",
    version="1.0.0",
    description="固定资产全生命周期管理系统",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.2.7:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

uploads_dir = os.path.join(os.path.dirname(__file__), "..", "uploads", "qrcode")
os.makedirs(uploads_dir, exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), "..", "uploads", "photos"), exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), "..", "uploads", "check"), exist_ok=True)
app.mount("/uploads", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "uploads")), name="uploads")

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "固定资产管理系统 API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)