from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class UserSignup(BaseModel):
    first_name: str
    last_name: str
    password: str
    method: str  # "email" or "phone"
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    @validator("email", always=True)
    def validate_email(cls, v, values):
        if values.get("method") == "email" and not v:
            raise ValueError("Email is required when method='email'")
        return v

    @validator("phone", always=True)
    def validate_phone(cls, v, values):
        if values.get("method") == "phone" and not v:
            raise ValueError("Phone is required when method='phone'")
        return v

class UserLogin(BaseModel):
    identifier: str  # email or phone
    method: str      # "email" or "phone"
    password: str


class SendOtpRequest(BaseModel):
    method: str  # "email" or "phone"
    contact: str  # email or phone

class VerifyOtpRequest(BaseModel):
    contact: str
    otp: str
