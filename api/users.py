import logging
from fastapi import Depends, APIRouter, File, UploadFile

from requests import FavoriteRequest

from controllers import (
    add_favlist_to_user,
    remove_favorite_from_user,
    get_current_active_user,
    get_user_favorites,
    update_profile_picture,
)
from models import User
from mongodb import get_nosql_db, MongoClient

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/favorites", tags=["User"])
async def alter_favorite_room(
    request: FavoriteRequest,
    current_user: User = Depends(get_current_active_user),
    client: MongoClient = Depends(get_nosql_db),
):
    """
    Add or remove a favorite room from a user
    the request.type should be either "add" or "remove"
    """
    try:
        if request.type == "add":
            new_user_obj = await add_favlist_to_user(request.username, request.favorites)
        elif request.type == "remove":
            new_user_obj = await remove_favorite_from_user(request.username, request.favorite)

        logger.info(f"Updated User Favorites\n{new_user_obj['favorites']}\n-----------------------")
        return new_user_obj
    except Exception as e:
        logger.error(f"/favorites: {e}")
        pass


@router.get("/favorites", tags=["User"])
async def get_favorite_rooms(
    current_user: User = Depends(get_current_active_user),
    client: MongoClient = Depends(get_nosql_db),
):
    """
    Get all favorite Room objects from a user
    """
    try:
        rooms_list = await get_user_favorites(current_user.username)
        return rooms_list
    except Exception as e:
        logger.error(f"/favorites: {e}")


@router.post("/user/profile_picture", tags=["User"])
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    client: MongoClient = Depends(get_nosql_db),
):
    """
    Upload a profile picture for the current user
    """
    try:
        new_user = await update_profile_picture(current_user, file.file, file.filename)
        return new_user
    except Exception as e:
        logger.error(f"POST /user/profile_picture: {e}")
