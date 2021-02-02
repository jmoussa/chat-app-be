from fastapi import APIRouter

from api.rooms import router as room_router

router = APIRouter()
router.include_router(room_router)
