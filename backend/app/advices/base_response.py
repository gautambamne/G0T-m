from typing import Any
from fastapi.responses import JSONResponse
from app.advices.response import (
    ApiErrorSchema,
    SuccesResponseSchema,
    ErrorResponseSchema
)


class BaseResponse:
    """Base response class to standardize API responses."""

    @staticmethod
    def succes_response(
        data: Any,
        status_code: int = 200
    )-> JSONResponse:
        """Generate a successful Api Response"""
        response_schema = SuccesResponseSchema(data=data)
        return JSONResponse(
            status_code=status_code,
            content=response_schema.model_dump(mode="json")
        )
    
    @staticmethod
    def error_response(
        status_code: int,
        message: str,
        errors: dict[str, str] | None = None
    ) -> JSONResponse:
        """Generate an error Api Response"""
        api_error = ApiErrorSchema(
            status_code=status_code,
            message=message,
            errors=errors
        )
        response_schema = ErrorResponseSchema(api_error=api_error)
        return JSONResponse(
            status_code=status_code,
            content=response_schema.model_dump(mode="json")
        )
    
    @staticmethod
    def created_response(
        data: Any = None
    ) -> JSONResponse:
        """Generate a 201 Created Api Response"""
        response = SuccesResponseSchema(data=data)
        return JSONResponse(
            status_code=201,
            content=response.model_dump(mode="json")
        )
    
    
    @staticmethod
    def not_found_response(message: str = "Resource not found") -> JSONResponse:
        """
        Create a 404 Not Found response.
        :param message: Error message (default: "Resource not found")
        :return: JSONResponse with 404 status code
        """
        return BaseResponse.error_response(message=message, status_code=404)

    @staticmethod
    def unauthorized_response(message: str = "Unauthorized") -> JSONResponse:
        """
        Create a 401 Unauthorized response.
        :param message: Error message (default: "Unauthorized")
        :return: JSONResponse with 401 status code
        """
        return BaseResponse.error_response(message=message, status_code=401)

    @staticmethod
    def forbidden_response(message: str = "Forbidden") -> JSONResponse:
        """
        Create a 403 Forbidden response.
        :param message: Error message (default: "Forbidden")
        :return: JSONResponse with 403 status code
        """
        return BaseResponse.error_response(message=message, status_code=403)

    @staticmethod
    def conflict_response(message: str = "Resource already exists") -> JSONResponse:
        """
        Create a 409 Conflict response.
        :param message: Error message (default: "Resource already exists")
        :return: JSONResponse with 409 status code
        """
        return BaseResponse.error_response(message=message, status_code=409)

    @staticmethod
    def validation_error_response(errors: dict) -> JSONResponse:
        """
        Create a 422 Validation Error response.
        :param errors: Validation error details
        :return: JSONResponse with 422 status code
        """
        return BaseResponse.error_response(
            message="Validation Error", status_code=422, errors=errors
        )

    @staticmethod
    def internal_server_error_response(
        message: str = "Internal Server Error",
    ) -> JSONResponse:
        """
        Create a 500 Internal Server Error response.
        :param message: Error message (default: "Internal Server Error")
        :return: JSONResponse with 500 status code
        """
        return BaseResponse.error_response(message=message, status_code=500)