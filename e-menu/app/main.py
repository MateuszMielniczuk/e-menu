from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.default import router as default_router
from app.api.v1.routers import router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(default_router)
app.include_router(router, prefix=settings.API_V1_PREFIX)
