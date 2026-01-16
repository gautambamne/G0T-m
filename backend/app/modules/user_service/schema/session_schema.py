from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class SessionSchema(BaseModel):
    """Schema for session information"""
    model_config = ConfigDict(from_attributes=True)
    # config_dict = ConfigDict defines how that data should behave

    id: UUID
    user_agent: str | None = None
    ip_address: str | None = None
    expires_at: datetime
    created_at: datetime
    updated_at: datetime

class SessionListSchema(BaseModel):
    """Schema for creating a new session"""
    sessions: list[SessionSchema]
    total: int