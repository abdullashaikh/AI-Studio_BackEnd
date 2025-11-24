import os

# All folder paths
folders = [
    "backend/app",
    "backend/app/auth",
    "backend/app/routers",
    "backend/app/db",
    "backend/app/utils",
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"Created folder: {folder}")

# --- File contents ---

main_py = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth.routes import router as auth_router

app = FastAPI(title="AI Studio Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
"""

config_py = """import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "AI Studio Backend"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecret")
    JWT_ALGORITHM: str = "HS256"

settings = Settings()
"""

auth_routes_py = """from fastapi import APIRouter

router = APIRouter()

@router.post("/signup")
async def signup():
    return {"message": "Signup endpoint works"}

@router.post("/login")
async def login():
    return {"message": "Login endpoint works"}
"""

init_py = """# Auto-generated"""

logger_py = """import logging

logger = logging.getLogger("ai_studio")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)
"""

requirements_txt = """fastapi
uvicorn[standard]
python-multipart
sqlalchemy
psycopg2-binary
pymongo
motor
python-jose[cryptography]
passlib[bcrypt]
pillow
pytesseract
pdf2image
weaviate-client
python-dotenv
redis
rq
requests
"""

# --- File creation mapping ---
files = {
    "backend/app/main.py": main_py,
    "backend/app/config.py": config_py,
    "backend/app/auth/routes.py": auth_routes_py,
    "backend/app/auth/__init__.py": init_py,
    "backend/app/routers/__init__.py": init_py,
    "backend/app/db/__init__.py": init_py,
    "backend/app/utils/__init__.py": init_py,
    "backend/app/utils/logger.py": logger_py,
    "backend/requirements.txt": requirements_txt
}

# Write all files
for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        print(f"Created file: {path}")

print("\n🎉 Backend folder structure created successfully!")
print("Next step: create virtual environment and run backend.")
