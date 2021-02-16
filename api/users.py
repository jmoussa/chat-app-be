import logging

from fastapi import Depends, APIRouter

from requests import FavoriteRequest

from controllers import (
    add_favlist_to_user,
    remove_favlist_to_user,
    get_current_active_user,
)
from models import User
from mongodb import get_nosql_db, MongoClient

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/favorites", tags=["User"])
async def add_favorite_room(
    request: FavoriteRequest,
    current_user: User = Depends(get_current_active_user),
    client: MongoClient = Depends(get_nosql_db),
):
    """
    Add or remove a favorite room from a user
    """
    try:
        if request.type == "add":
            new_user_obj = await add_favlist_to_user(request.username, request.favorites)
        elif request.type == "remove":
            new_user_obj = await remove_favlist_to_user(request.username, request.favorite)

        return new_user_obj
    except Exception as e:
        logger.error(f"/favorites: {e}")
        pass
