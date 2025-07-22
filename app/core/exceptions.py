from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)


class RaadiException(Exception):
    """Base exception class for Raadi application"""
    
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(RaadiException):
    """Authentication related errors"""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401)


class AuthorizationError(RaadiException):
    """Authorization related errors"""
    
    def __init__(self, message: str = "Access denied"):
        super().__init__(message, 403)


class ValidationError(RaadiException):
    """Validation related errors"""
    
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, 422)


class NotFoundError(RaadiException):
    """Resource not found errors"""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)


class ConflictError(RaadiException):
    """Resource conflict errors"""
    
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(message, 409)


async def raadi_exception_handler(request: Request, exc: RaadiException):
    """Handle custom Raadi exceptions"""
    logger.error(f"RaadiException: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "status_code": exc.status_code,
            "type": exc.__class__.__name__
        }
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTPException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "type": "HTTPException"
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation exceptions"""
    logger.error(f"ValidationError: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation failed",
            "details": exc.errors(),
            "status_code": 422,
            "type": "ValidationError"
        }
    )


def setup_exception_handlers(app):
    """Setup exception handlers for the FastAPI app"""
    app.add_exception_handler(RaadiException, raadi_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
