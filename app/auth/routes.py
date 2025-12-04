from fastapi import APIRouter, HTTPException, status
from app.db.mongo import users_collection
from .models import UserSignup, UserLogin
from .utils import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from app.utils.otp_utils import generate_otp, otp_expiry_time

from app.db.mongo import otp_collection, users_collection
from .models import SendOtpRequest, VerifyOtpRequest
from app.utils.email_otp import send_email_otp
from app.utils.twilio_client import send_sms_otp

import datetime
router = APIRouter()
# ---------------- SIGNUP --------------------
@router.post("/signup")
async def signup(payload: UserSignup):
    print("Signup payload:", payload)
    # Decide which contact to validate (email or phone)
    contact = payload.email if payload.method == "email" else payload.phone
    print("Contact for signup:", contact)
    if not contact:
        raise HTTPException(status_code=400, detail="Contact (email/phone) is required.")
   
    # --------- OTP Verification ----------
    otp_record = await otp_collection.find_one({"contact": contact})
    print("OTP record found:", otp_record)
    if otp_record:
        raise HTTPException(status_code=400, detail="Please verify OTP first")

    # --------- Check If User Exists ---------
    query = {"email": payload.email} if payload.method == "email" else {"phone": payload.phone}

    existing = await users_collection.find_one(query)
    print("Existing user found:", existing)
    if existing:
        raise HTTPException(status_code=400, detail="User already registered")

    # --------- Prepare User Data ----------
    user_data = {
        "first_name": payload.first_name,
        "last_name": payload.last_name,
        "password": hash_password(payload.password)
    }

    if payload.method == "email":
        user_data["email"] = payload.email.lower()
    else:
        user_data["phone"] = payload.phone

    # --------- Save User ----------
    await users_collection.insert_one(user_data)

    return {"message": "User registered successfully"}



# ---------------- LOGIN --------------------
@router.post("/login")
async def login(payload: UserLogin):

    identifier = payload.identifier
    method = payload.method

    # check by email or phone
    query = {"email": identifier} if method == "email" else {"phone": identifier}

    user = await users_collection.find_one(query)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": identifier})

    return {
        "message": "Login successful",
        "access_token": token,
        "user": {
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user.get("email"),
            "phone": user.get("phone")
        }
    }




# ---------------- SEND OTP --------------------
@router.post("/send-otp")
async def send_otp(payload: SendOtpRequest):

    contact = payload.contact

    # Check if already registered
    existing = await users_collection.find_one({"email": contact})
    if existing:
        raise HTTPException(status_code=400, detail="User already registered")

    otp = generate_otp()

    otp_entry = {
        "contact": contact,
        "otp": otp,
        "expires_at": otp_expiry_time(),
    }

    # Remove old OTP if exists
    await otp_collection.delete_many({"contact": contact})
    await otp_collection.insert_one(otp_entry)

    # ------------------ Send Email ------------------
    if payload.method == "email":
        try:
            send_email_otp(contact, otp)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Email error: {str(e)}")

    # ------------------ Send SMS via Twilio ------------------
    elif payload.method == "phone":
        try:
            send_sms_otp(contact, otp)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Twilio error: {str(e)}")

    else:
        raise HTTPException(status_code=400, detail="Invalid method (email/phone)")

    return {"message": "OTP sent successfully"}


# ---------------- VERIFY OTP --------------------
@router.post("/verify-otp")
async def verify_otp(payload: VerifyOtpRequest):

    record = await otp_collection.find_one({"contact": payload.contact})
    if not record:
        raise HTTPException(status_code=400, detail="OTP not found")

    # Check expiry
    if record["expires_at"] < datetime.datetime.utcnow():
        await otp_collection.delete_many({"contact": payload.contact})
        raise HTTPException(status_code=400, detail="OTP expired")

    if record["otp"] != payload.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # OTP valid → delete it
    await otp_collection.delete_many({"contact": payload.contact})

    return {"message": "OTP verified successfully"}
