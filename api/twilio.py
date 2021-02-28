import logging
import config
from fastapi import Depends, APIRouter
from controllers import get_current_active_user
from models import User
from mongodb import get_nosql_db, MongoClient
from models import Token
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/twilio/token/{room_name}", tags=["Video Chat"], response_model=Token)
async def login_for_access_token(
    room_name,
    db: MongoClient = Depends(get_nosql_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Twilio Token Generator
    """
    token = AccessToken(config.ACCOUNT_SID, config.API_KEY_SID, config.API_KEY_SECRET)
    token.identity = current_user.username
    grant = VideoGrant(room=room_name)
    token.add_grant(grant)
    jwt = token.to_jwt()
    logger.info(jwt)
    return jwt
