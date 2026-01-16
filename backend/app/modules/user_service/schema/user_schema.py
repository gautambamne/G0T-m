import re      #Regular Expression module 
from pydantic import BaseModel, Field, field_validator

class UpdateUserSchema(BaseModel):
    """Schema for updating user information."""
    name: str | None = Field(
        None, min_length=2, max_length=255
    )

class ChangePasswordSchema(BaseModel):
    """Schema for changing user password"""
    current_password: str = Field(
        ..., min_length=6, max_length=100
    )
    new_password: str = Field(
        ..., min_length=6, max_length=100
    )

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v:str) -> str:
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$', v):
            raise ValueError("Password must be at least 6 characters long and contain both letters and numbers.")
        return v