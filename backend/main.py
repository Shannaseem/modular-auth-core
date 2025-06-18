import sys
import os
import re
import logging
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Depends, Form, File, UploadFile
from typing import Optional
import shutil

# Add Tutex/ to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, Form, Request, Depends, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from typing import Literal, Optional
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import User
from passlib.context import CryptContext
import shutil

app = FastAPI()

# Configure Jinja2 templates
templates = Jinja2Templates(directory="../frontend/templates")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic model for login form validation
class LoginForm(BaseModel):
    username: str
    password: str
    user_type: Optional[Literal["student", "tutor", "admin"]] = "student"

# Pydantic model for registration
class RegisterForm(BaseModel):
    username: str
    password: str
    user_type: str
    full_name: str
    phone_number: str
    email: Optional[str] = None
    fathers_name: Optional[str] = None
    last_qualification: Optional[str] = None
    register_as_parent: Optional[bool] = False

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/login")
async def get_login_page(request: Request, error: Optional[str] = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@app.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    user_type: Optional[str] = Form("student"),
    db: Session = Depends(get_db)
):
    user_type_normalized = user_type.capitalize() if user_type else "Student"
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        return RedirectResponse(url="/login?error=Invalid username or password", status_code=303)
    if user.user_type != user_type_normalized:
        return RedirectResponse(url="/login?error=Invalid user type", status_code=303)
    if not user.is_verified:
        return RedirectResponse(url="/login?error=Please verify your account with OTP", status_code=303)
    return RedirectResponse(url="/dashboard", status_code=303)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.post("/signup")
async def signup(
    username: str = Form(...),
    password: str = Form(...),
    user_type: str = Form(...),
    full_name: str = Form(...),
    phone_number: str = Form(...),
    email: str = Form(None),
    fathers_name: Optional[str] = Form(None),
    last_qualification: Optional[str] = Form(None),
    register_as_parent: Optional[bool] = Form(False),
    cnic_front: UploadFile = File(None),
    cnic_back: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    logger.debug(f"Received signup request for username: {username}, user_type: {user_type}")

    # Check if username exists
    if db.query(User).filter(User.username == username).first():
        logger.warning(f"Username {username} already exists")
        return JSONResponse(status_code=400, content={"error": "Username already exists"})
    
    # Validate user_type
    if user_type.capitalize() not in ["Student", "Tutor", "Admin"]:
        logger.warning(f"Invalid user_type: {user_type}")
        return JSONResponse(status_code=400, content={"error": "Invalid user type"})
    
    # Ensure uploads directory exists
    uploads_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "static", "uploads"))
    logger.debug(f"Uploads directory: {uploads_dir}")
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Save CNIC files if provided (required for Tutor)
    cnic_front_path = None
    cnic_back_path = None
    if user_type.lower() == "tutor":
        if not (cnic_front and cnic_back):
            logger.warning("CNIC images missing for tutor")
            return JSONResponse(status_code=400, content={"error": "CNIC images required for tutors"})
        # Sanitize filenames
        front_filename = re.sub(r'[^a-zA-Z0-9._-]', '_', cnic_front.filename)
        back_filename = re.sub(r'[^a-zA-Z0-9._-]', '_', cnic_back.filename)
        cnic_front_path = os.path.join("backend", "static", "uploads", f"{username}_cnic_front_{front_filename}").replace("\\", "/")
        cnic_back_path = os.path.join("backend", "static", "uploads", f"{username}_cnic_back_{back_filename}").replace("\\", "/")
        cnic_front_abs_path = os.path.abspath(os.path.join(uploads_dir, f"{username}_cnic_front_{front_filename}"))
        cnic_back_abs_path = os.path.abspath(os.path.join(uploads_dir, f"{username}_cnic_back_{back_filename}"))
        logger.debug(f"Saving CNIC front to: {cnic_front_abs_path}")
        logger.debug(f"Saving CNIC back to: {cnic_back_abs_path}")
        try:
            # Reset file pointer and save
            await cnic_front.seek(0)
            with open(cnic_front_abs_path, "wb") as f:
                shutil.copyfileobj(cnic_front.file, f)
            logger.debug(f"CNIC front saved: {cnic_front_abs_path}")
            await cnic_back.seek(0)
            with open(cnic_back_abs_path, "wb") as f:
                shutil.copyfileobj(cnic_back.file, f)
            logger.debug(f"CNIC back saved: {cnic_back_abs_path}")
        except Exception as e:
            logger.error(f"Failed to save CNIC files: {str(e)}")
            return JSONResponse(status_code=500, content={"error": f"Failed to save CNIC files: {str(e)}"})
    
    # Hash password and save user
    hashed_password = pwd_context.hash(password)
    user = User(
        username=username,
        hashed_password=hashed_password,
        user_type=user_type.capitalize(),
        full_name=full_name,
        phone_number=phone_number,
        email=email,
        fathers_name=fathers_name,
        last_qualification=last_qualification,
        register_as_parent=register_as_parent,
        cnic_front_path=cnic_front_path,
        cnic_back_path=cnic_back_path,
        is_verified=False
    )
    try:
        db.add(user)
        db.commit()
        logger.debug(f"User {username} added to database")
    except Exception as e:
        logger.error(f"Database commit failed: {str(e)}")
        # Cleanup files if saved
        if cnic_front_path and os.path.exists(cnic_front_abs_path):
            os.remove(cnic_front_abs_path)
        if cnic_back_path and os.path.exists(cnic_back_abs_path):
            os.remove(cnic_back_abs_path)
        return JSONResponse(status_code=500, content={"error": f"Database error: {str(e)}"})
    
    return JSONResponse(content={"message": "Registration successful, OTP sent"})

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/")
async def root():
    return {"message": "TutEx Backend Running"}