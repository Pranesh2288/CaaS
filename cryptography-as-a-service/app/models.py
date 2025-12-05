from pydantic import BaseModel, EmailStr
from typing import Optional, List, Union
from datetime import datetime
from bson import ObjectId # Used for MongoDB ID type

# --- MongoDB Document Models ---

class PyObjectId(ObjectId):
    """
    Custom type for MongoDB ObjectId serialization with Pydantic.
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class UserDocument(BaseModel):
    """Schema for data stored in the 'users' MongoDB collection."""
    id: Optional[PyObjectId] = None  # MongoDB ObjectId
    username: str
    email: EmailStr
    password_hash: str
    rsa_public_key: Optional[str] = None # PEM format

    class Config:
        # Allows Pydantic to handle MongoDB's _id field
        json_encoders = {
            ObjectId: str
        }
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        
class FileMetadataDocument(BaseModel):
    """Schema for data stored in the 'files' MongoDB collection."""
    id: Optional[PyObjectId] = None # MongoDB ObjectId
    owner: str # Username or User ID
    filename: str
    gcs_path: str
    # Encrypted session key, nonce, and tag stored as binary/bytes
    encrypted_aes_key: bytes
    nonce: bytes
    tag: bytes
    
    class Config:
        json_encoders = {
            ObjectId: str
        }
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class SessionDocument(BaseModel):
    """Schema for temporary session data, primarily for OTP verification."""
    id: Optional[PyObjectId] = None 
    user_id: str
    otp_signature: bytes
    expiry_time: datetime

    class Config:
        json_encoders = {
            ObjectId: str
        }
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

# --- API Request/Response Models ---

class UserRegister(BaseModel):
    """Model for user registration request."""
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """Model for user login request (step 1 of MFA)."""
    username: str
    password: str

class OTPVerify(BaseModel):
    """Model for OTP verification request (step 2 of MFA)."""
    username: str
    otp_code: str

class TokenResponse(BaseModel):
    """Model for returning a successful JWT to the client."""
    access_token: str
    token_type: str = "bearer"

class ErrorResponse(BaseModel):
    """Model for returning standardized error messages."""
    detail: str