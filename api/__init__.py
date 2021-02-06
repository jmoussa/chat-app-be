from fastapi import APIRouter

from api.auth import router as auth_router
from api.rooms import router as room_router

router = APIRouter()
router.include_router(room_router)
router.include_router(auth_router)
