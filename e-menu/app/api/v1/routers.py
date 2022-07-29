from fastapi import APIRouter

from app.api.v1.endpoints import dish, menu_card, user

router = APIRouter()

router.include_router(menu_card.router, prefix="/menu_card", tags=["menu card"])
router.include_router(dish.router, prefix="/dish", tags=["dish"])
router.include_router(user.router, prefix="/user", tags=["user"])
