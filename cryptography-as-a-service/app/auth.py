from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt

# Load environment variables for security configuration
import os
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
# Cryptography Context for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key") # Use a strong key from env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme for dependency injection in protected routes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- Password Hashing ---

def get_password_hash(password: str) -> str:
    """Hashes a plaintext password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

# --- JWT Token Management ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "sub": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user_username(token: str = Depends(oauth2_scheme)) -> str:
    """
    Decodes the JWT and validates the user. Used as a FastAPI Dependency.
    
    Raises:
        HTTPException: If the token is invalid or expired.
    
    Returns:
        str: The username stored in the token payload.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") # Assuming we store the username in 'sub'
        
        if username is None:
            raise credentials_exception
            
        # In a real application, you would check if the user exists in the DB here
        
    except JWTError:
        raise credentials_exception
        
    return username