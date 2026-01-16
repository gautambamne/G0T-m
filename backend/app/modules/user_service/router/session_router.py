from uuid import UUID
from fastapi import APIRouter, Depends, Cookie
from app.modules.user_service.schema.session_schema import SessionListSchema
from app.advices.response import SuccesResponseSchema, MessageSchema
from app.advices.base_response import BaseResponse
from app.modules.user_service.service.session_service import SessionService, get_session_service
from app.middlewares.dependencies import get_current_user, CurrentUser

router = APIRouter()

@router.get(
    "/",
    summary="Get current user sessions",
    response_model=SuccesResponseSchema[SessionListSchema]
)
async def get_sessions(
    current_user: CurrentUser = Depends(get_current_user),
    service: SessionService = Depends(get_session_service)
):
    result = await service.get_user_sessions(current_user.id)
    return BaseResponse.succes_response(data=result)

@router.delete(
    "/{session_id}",
    summary="Delete user session",
    response_model=SuccesResponseSchema[MessageSchema]
)
async def delete_session(
    session_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    service: SessionService = Depends(get_session_service)
):
    await service.delete_session(session_id)
    return BaseResponse.succes_response(data={"message": "Session deleted successfully"})

@router.delete(
    "/all",
    summary="Delete all user sessions",
    response_model=SuccesResponseSchema[MessageSchema]
)
async def delete_all_sessions(
    current_user: CurrentUser = Depends(get_current_user),
    refresh_token: str = Cookie(None),
    service: SessionService = Depends(get_session_service)
):
    await service.delete_all_sessions(current_user.id, refresh_token)
    return BaseResponse.succes_response(data={"message": "All sessions deleted successfully"})
