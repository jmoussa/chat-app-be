from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class RoomCreateRequest(BaseModel):
    username: str
    room_name: str
