from fastapi import APIRouter, Depends
from app.modules.user_service.schema.auth_schema import ReturnUserSchema
from app.modules.user_service.schema.user_schema import UpdateUserSchema,ChangePasswordSchema
from app.advices.base_response import BaseResponse
from app.advices.response import SuccesResponseSchema, MessageSchema
from app.modules.user_service.service.user_services import UserProfileService, get_user_profile_service
from app.middlewares.dependencies  import get_current_user, CurrentUser

router = APIRouter()

@router.get(
    "/me",
    summary="Get current user profile",
    response_model=SuccesResponseSchema[CurrentUser]
)
async def get_me(
    current_user: CurrentUser = Depends(get_current_user)
):
    return BaseResponse.succes_response(data=current_user)

@router.put(
    "/me",
    summary="Update current user profile",
    response_model=SuccesResponseSchema[ReturnUserSchema]
)
async def update_me(
    data: UpdateUserSchema,
    current_user: CurrentUser = Depends(get_current_user),
    service: UserProfileService = Depends(get_user_profile_service)
):
    result = await service.update_user_profile(
        user_id=current_user.id,
        data=data
    )
    return BaseResponse.succes_response(data=result)


@router.post(
    "/me/change-password",
    summary="Change user password",
    response_model=SuccesResponseSchema[MessageSchema]
)
async def change_password(
    data: ChangePasswordSchema,
    current_user: CurrentUser = Depends(get_current_user),
    service: UserProfileService = Depends(get_user_profile_service)
):
    await service.change_password(current_user.id, data)
    return BaseResponse.succes_response(data={"message": "Password changed successfully"})


@router.delete(
    "/me",
    summary="Delete user account",
    response_model=SuccesResponseSchema[MessageSchema]
)
async def delete_account(
    current_user: CurrentUser = Depends(get_current_user),
    service: UserProfileService = Depends(get_user_profile_service)
):
    await service.delete_account(current_user.id)
    return BaseResponse.succes_response(data={"message": "Account deleted successfully"})
