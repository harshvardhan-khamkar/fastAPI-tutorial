from fastapi import FastAPI, HTTPException, status
from models import UserCreate, UserUpdate, UserOut
from db import db
from bson import ObjectId

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    result = await db.users.insert_one(user.dict())
    return {
        "id": str(result.inserted_id),
        **user.dict()
    }
@app.get("/users/{id}")
async def get_user(id: str):
    user = await db.users.find_one({"_id": ObjectId(id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user["id"] = str(user["_id"])
    del user["_id"]
    return user

@app.get("/users/")
async def list_users():
    users=[]
    cursor = db.users.find({})
    async for user in cursor:
        user["id"] = str(user["_id"])
        del user["_id"]
        users.append(user)

    return users

@app.put("/users/{id}")
async def update_user(id: str, user: UserUpdate):
    result = await db.users.update_one(
        {"_id": ObjectId(id)},
        {"$set": {k: v for k, v in user.dict().items() if v is not None}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"msg": "updated"}
@app.delete("/users/{id}")
async def delete_user(id: str):
    result = await db.users.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"msg": "deleted"}
