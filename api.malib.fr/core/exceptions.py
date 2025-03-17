from fastapi.exceptions import StarletteHTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from slowapi.errors import RateLimitExceeded
from pydantic.error_wrappers import ValidationError

def unexpected_handler(request, exc):
    return JSONResponse(status_code=500, content={"error":500})

def request_validation_handler(request, exc):
    return JSONResponse(status_code=422, content={"error":422})

def validation_handler(request, exc):
    return JSONResponse(status_code=422, content={"error":422})

def rate_handler(request, exc):
    return JSONResponse(status_code=429, content={"error":429})

def universal_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"error":exc.status_code})

def jwt_handler(request, exc):
    return JSONResponse(status_code=444, content={"error":444})

def init(app):
    app.add_exception_handler(Exception, unexpected_handler)
    app.add_exception_handler(RateLimitExceeded, rate_handler)
    app.add_exception_handler(RequestValidationError, request_validation_handler)
    app.add_exception_handler(ValidationError, validation_handler)
    app.add_exception_handler(AuthJWTException, jwt_handler)
    app.add_exception_handler(StarletteHTTPException, universal_handler)




