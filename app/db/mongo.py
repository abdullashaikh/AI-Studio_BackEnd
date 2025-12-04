from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client["AI_STUDIO"]  # your database name
users_collection = db["users"]
otp_collection = db["otp_codes"]
otp_phone_collection = db["phone_otps"]
