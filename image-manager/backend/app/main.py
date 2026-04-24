from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from .database import engine, Base, get_db
from .models import Image
from .schemas import ImageList, ImageOut
from .config import settings
from .storage.local import LocalStorage
from .storage.oss import OSSStorage
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

app = FastAPI(title="Image Manager API")

# 初始化存储
if settings.STORAGE_TYPE == "oss":
    storage = OSSStorage(settings.OSS_ENDPOINT, settings.OSS_BUCKET, 
                         settings.OSS_ACCESS_KEY, settings.OSS_SECRET_KEY, 
                         settings.OSS_CDN_DOMAIN)
else:
    storage = LocalStorage()
    static_dir = Path("/app/data/images")
    static_dir.mkdir(exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/images/upload", response_model=list[ImageOut])
async def upload(files: list[UploadFile] = File(...), db: AsyncSession = Depends(get_db)):
    results = []
    for f in files:
        info = await storage.upload(f.file, f.filename)
        img = Image(filename=f.filename, object_key=info["key"], url=info["url"], size=info["size"])
        db.add(img)
        results.append(img)
    await db.commit()
    for r in results:
        await db.refresh(r)
    return results

@app.get("/images/", response_model=ImageList)
async def list_images(page: int = 1, limit: int = 20, db: AsyncSession = Depends(get_db)):
    offset = (page - 1) * limit
    total = await db.scalar(select(func.count(Image.id)))
    stmt = select(Image).order_by(Image.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(stmt)
    return {"items": result.scalars().all(), "total": total}

@app.delete("/images/{image_id}")
async def delete_image(image_id: int, db: AsyncSession = Depends(get_db)):
    img = await db.get(Image, image_id)
    if not img:
        raise HTTPException(404, "Image not found")
    await storage.delete(img.object_key)
    await db.delete(img)
    await db.commit()
    return {"status": "ok"}