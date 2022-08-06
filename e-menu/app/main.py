from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.default import router as default_router
from app.api.v1.routers import router
from app import settings

app = FastAPI(title=settings.APP_TITLE, description=settings.APP_DESCRIPTION)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(default_router)
app.include_router(router, prefix="/v1")
