import os
import hmac
import hashlib
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

PASSWORD_KEY = os.getenv("PASSWORD_KEY", "")  # your "pepper"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _derive_bytes(password: str) -> bytes:
    """
    Derive a fixed-length binary value from (password, pepper).
    We use HMAC-SHA256 with PASSWORD_KEY as key when pepper is present.
    Result is 32 bytes, safely < bcrypt's 72-byte limit.
    """
    pw_bytes = password.encode("utf-8")
    if PASSWORD_KEY:
        key = PASSWORD_KEY.encode("utf-8")
        return hmac.new(key, pw_bytes, hashlib.sha256).digest()
    # fallback: plain sha256 digest (32 bytes)
    return hashlib.sha256(pw_bytes).digest()


def hash_password(password: str) -> str:
    """
    Returns a bcrypt hash (string) of the derived bytes.
    Store this string in MongoDB.
    """
    data = _derive_bytes(password)
    return pwd_context.hash(data)


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify given password (with pepper) against stored bcrypt hash.
    """
    data = _derive_bytes(password)
    return pwd_context.verify(data, hashed)
