import logging
from config import ACCOUNT_SID, API_KEY_SID, API_KEY_SECRET
from fastapi import Depends, APIRouter
from controllers import get_current_active_user
from models import User
from mongodb import get_nosql_db, MongoClient
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/twilio/token/{room_name}", tags=["Video Chat"])
async def login_for_access_token(
    room_name, db: MongoClient = Depends(get_nosql_db), current_user: User = Depends(get_current_active_user),
):
    """
    Twilio Token Generator
    """
    try:
        token = AccessToken(ACCOUNT_SID, API_KEY_SID, API_KEY_SECRET)
        token.identity = current_user.username
        grant = VideoGrant(room=room_name)
        token.add_grant(grant)
        jwt = token.to_jwt()
        return {"accessToken": jwt}
    except Exception as ex:
        logger.error(ex)
        return ex
