
# Pydantic Schemas for API validation
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
import re

# User schemas
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    language_preference: str = Field(default="English")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if len(v) > 128:
            raise ValueError('Password must be no more than 128 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter (A-Z)')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter (a-z)')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit (0-9)')
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', v):
            raise ValueError('Password must contain at least one special character (!@#$%^&*() etc.)')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=128)

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    language_preference: Optional[str] = Field(None, max_length=50)

    @validator('language_preference')
    def validate_language(cls, v):
        if v and v not in ['English', 'Hindi', 'Spanish', 'French', 'German']:
            raise ValueError('Language must be one of: English, Hindi, Spanish, French, German')
        return v

class PasswordChange(BaseModel):
    current_password: str = Field(..., max_length=128)
    new_password: str = Field(..., min_length=8, max_length=128)

    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('New password must be at least 8 characters long')
        if len(v) > 128:
            raise ValueError('New password must be no more than 128 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('New password must contain at least one uppercase letter (A-Z)')
        if not re.search(r'[a-z]', v):
            raise ValueError('New password must contain at least one lowercase letter (a-z)')
        if not re.search(r'\d', v):
            raise ValueError('New password must contain at least one digit (0-9)')
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', v):
            raise ValueError('New password must contain at least one special character (!@#$%^&*() etc.)')
        return v

class UserResponse(UserBase):
    id: int
    user_id: str
    is_active: bool
    is_verified: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: dict

class LoginResponse(BaseModel):
    success: bool
    message: str
    data: Token

class RegisterResponse(BaseModel):
    success: bool
    message: str
    data: dict

# File analysis schemas
class FileAnalysisResponse(BaseModel):
    success: bool
    filename: str
    file_size: int
    analysis: dict
    message: str

class TextAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=10)

class TextAnalysisResponse(BaseModel):
    success: bool
    analysis: dict
    message: str