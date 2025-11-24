from fastapi import APIRouter, HTTPException, status
from app.db.mongo import users_collection
from .models import UserSignup, UserLogin
from .utils import hash_password, verify_password
from app.utils.jwt_handler import create_access_token

router = APIRouter()

# ---------------- SIGNUP --------------------
@router.post("/signup")
async def signup(payload: UserSignup):
    email = payload.email.lower()

    # Check if user exists
    existing = await users_collection.find_one({"email": email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = {
        "first_name": payload.first_name,
        "last_name": payload.last_name,
        "email": email,
        "password": hash_password(payload.password),
    }

    await users_collection.insert_one(user_data)

    return {"message": "User registered successfully"}


# ---------------- LOGIN --------------------
@router.post("/login")
async def login(payload: UserLogin):
    email = payload.email.lower()

    user = await users_collection.find_one({"email": email})
    print(user)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({"sub": email})

    return {
        "message": "Login successful",
        "access_token": token,
        "user": {
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"]
        }
    }
