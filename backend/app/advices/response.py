from datetime import datetime
from pydantic import BaseModel, Field
from typing import Dict, Generic, TypeVar, Optional

T = TypeVar("T")

class ApiErrorSchema(BaseModel):
    """ Schema for API error responses """
    status_code: int = Field(..., description="HTTP status code of the error")
    message: str = Field(..., description="Detailed error message")
    errors: Optional[Dict[str, str]] = Field(None, description="Additional error details")

class MessageSchema(BaseModel):
    """ Schema for simple message responses """
    message: str = Field(..., description="Response message")

class SuccesResponseSchema(BaseModel, Generic[T]):
    """ Schema for successfull API responses """
    local_date_time: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z",
        description="The local date and time when the response is generated in ISO 8601 format"
    )
    data: Optional[T] = None
    api_error: None = None

class ErrorResponseSchema(BaseModel):
    """ Schema for error API responses """
    local_date_time: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z",
        description="The local date and time when the response is generated in ISO 8601 format"
    )
    data: None = None
    api_error: ApiErrorSchema