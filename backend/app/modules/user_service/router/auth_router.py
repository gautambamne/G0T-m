from app.modules.user_service.schema.auth_schema import (
    LoginSchema,
    RegisterSchema,
    ResetPasswordSchema,
    VerifySchema,
    ReturnUserSchema,
    ForgotPasswordSchema,
    TokenResponseSchema,
    RefreshTokenSchema
)
from app.advices.response import SuccesResponseSchema, ErrorResponseSchema, MessageSchema
from app.modules.user_service.utils.auth_utils import CookieUtils
from fastapi import APIRouter, Depends, Query, Response, Cookie
from app.modules.user_service.service.auth_service import UserService, get_user_service
from app.advices.base_response import BaseResponse

router = APIRouter()

@router.post(
    "/register",
    summary="Register a new user",
    responses={
        200: {
            "description": "User registered successfully",
            "model": SuccesResponseSchema[ReturnUserSchema]
        },
        400: {
            "description": "User already exists",
            "model": ErrorResponseSchema
        },
        422: {
            "description": "Validation error",
            "model": ErrorResponseSchema
        }
    }
)
async def register(
    data: RegisterSchema, 
    service: UserService = Depends(get_user_service)
):
    result = await service.register(data)
    return BaseResponse.succes_response(data=result)

@router.post(
    "/login",
    summary="Login user",
    response_model=SuccesResponseSchema[TokenResponseSchema]
)
async def login(
    response: Response,
    data: LoginSchema,
    service: UserService = Depends(get_user_service)
):
    result = await service.login(data)
    CookieUtils.set_auth_cookies(response, result.access_token, result.refresh_token)
    return BaseResponse.succes_response(data=result)

@router.post(
    "/verify",
    summary="Verify user email",
    response_model=SuccesResponseSchema[TokenResponseSchema]
)
async def verify_user(
    response: Response,
    data: VerifySchema,
    service: UserService = Depends(get_user_service)
):
    result = await service.verify_user(data)
    CookieUtils.set_auth_cookies(response, result.access_token, result.refresh_token)
    return BaseResponse.succes_response(data=result)

@router.post(
    "/refresh",
    summary="Refresh access token",
    response_model=SuccesResponseSchema[RefreshTokenSchema]
)
async def refresh_token(
    response: Response,
    refresh_token: str = Cookie(None, description="Refresh token from cookie"),
    service: UserService = Depends(get_user_service)
):
    result = await service.refresh_token(refresh_token)
    # Update access token cookie only
    response.set_cookie(
        key="access_token",
        value=result.access_token,
        max_age=30 * 60,
        httponly=True,
        samesite="lax",
        path="/",
    )
    return BaseResponse.succes_response(data=result)

@router.post(
    "/forgot-password",
    summary="Request password reset",
    response_model=SuccesResponseSchema[MessageSchema]
)
async def forgot_password(
    data: ForgotPasswordSchema,
    service: UserService = Depends(get_user_service)
):
    await service.forgot_password(data)
    return BaseResponse.succes_response(data={"message": "Password reset code sent to email"})

@router.post(
    "/verify-code",
    summary="Verify reset code is valid",
    response_model=SuccesResponseSchema[MessageSchema]
)
async def verify_code(
    email: str = Query(..., description="User email"),
    code: str = Query(..., description="Verification code"),
    service: UserService = Depends(get_user_service)
):
    await service.verify_code_valid(email, code)
    return BaseResponse.succes_response(data={"message": "Verification code is valid"})

@router.post(
    "/reset-password",
    summary="Reset password with verification code",
    response_model=SuccesResponseSchema[MessageSchema]
)
async def reset_password(
    data: ResetPasswordSchema,
    service: UserService = Depends(get_user_service)
):
    await service.reset_password(data)
    return BaseResponse.succes_response(data={"message": "Password reset successfully"})

@router.post(
    "/logout",
    summary="Logout user",
    response_model=SuccesResponseSchema[MessageSchema]
)
async def logout(
    response: Response,
    refresh_token: str = Cookie(None, description="Refresh token from cookie"),
    service: UserService = Depends(get_user_service)
):
    await service.logout(refresh_token)
    CookieUtils.clear_auth_cookies(response)
    return BaseResponse.succes_response(data={"message": "Logged out successfully"})