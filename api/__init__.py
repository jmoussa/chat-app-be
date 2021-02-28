from fastapi import APIRouter

from api.auth import router as auth_router
from api.rooms import router as room_router
from api.users import router as user_router
from api.twilio import router as twilio_router

router = APIRouter()
router.include_router(room_router)
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(twilio_router)
