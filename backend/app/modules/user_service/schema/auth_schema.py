from app.exceptions.exceptions import ConflictException
from uuid import UUID
from pydantic import BaseModel, field_validator, EmailStr, Field, ConfigDict
from datetime import datetime
import re 


class RegisterSchema(BaseModel):
    """ SChema for user registration """
    name: str = Field(..., min_length=2, max_length=50, examples=["John Doe"])
    email: EmailStr = Field(..., examples=["johndoe@example.com"])
    password: str = Field(..., min_length=6, max_length=100, examples=["Password123"])

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&.#^()_+\-=\[\]{};:,<>]).{6,}$', v):
            raise ConflictException("Password must be at least 6 characters long and contain at least one letter, one number, and one special character.")
        return v
    
class ReturnUserSchema(BaseModel):
    """ Schema for returning user information """
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: EmailStr
    is_verified: bool
    created_at: datetime
    updated_at: datetime

class LoginSchema(BaseModel):
    """ Schema for user login """
    email: EmailStr = Field(..., examples=["johndoe@example.com"])
    password: str = Field(..., min_length=6, max_length=100, examples=["Password123"])

class VerifySchema(BaseModel):
    """ Schema for email verification """
    email: EmailStr = Field(..., examples=["johndoe@example.com"])
    verification_code: str = Field(..., min_length=6, max_length=6, examples=["123456"])

class ResetPasswordSchema(BaseModel):
    """ Schema for resetting password """
    email: EmailStr = Field(..., examples=["johndoe@example.com"])
    verification_code: str = Field(..., min_length=6, max_length=6, examples=["123456"])
    password: str = Field(..., min_length=6, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&.#^()_+\-=\[\]{};:,<>]).{6,}$', v):
            raise ConflictException("Password must be at least 6 characters long and contain at least one letter, one number, and one special character.")
        return v
    
class ForgotPasswordSchema(BaseModel):
    """ Schema for forgot password """
    email: EmailStr = Field(..., examples=["johndoe@example.com"])

class TokenResponseSchema(BaseModel):
    """ Schema for token response """
    access_token: str
    refresh_token: str
    user: ReturnUserSchema

class RefreshTokenSchema(BaseModel):
    """ Schema for refresh token """
    access_token: str
    user: ReturnUserSchema