from fastapi import APIRouter
from app.db import db
from app.models.user import UserModel

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate):
    result = await db.users.insert_one(user.dict())
    new_user = await db.users.find_one({"_id": result.inserted_id})
    return new_user
    