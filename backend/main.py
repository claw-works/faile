from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import image, doc

app = FastAPI(title="faile API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(image.router, prefix="/api/image")
app.include_router(doc.router, prefix="/api/doc")
