from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .controllers import users 
from fastapi import FastAPI, HTTPException, Request, status

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom exception handler for FastAPI to catch RequestValidationError.

    This function is triggered whenever FastAPI detects a validation error
    during the request processing (e.g., if the request body or query parameters 
    don't meet the schema requirements defined in the endpoint). The exception 
    handler captures the error, formats a custom JSON response, and sends it back 
    to the client with an HTTP 422 Unprocessable Entity status code.

    Parameters:
    ----------
    request : Request
        The incoming HTTP request object that triggered the validation error. 
        This contains information about the request (such as the URL, method, 
        headers, and body).
        
    exc : RequestValidationError
        The validation exception object raised by FastAPI. It contains details
        about the validation error, including the error message and the invalid 
        data that caused the exception.

    Returns:
    -------
    JSONResponse
        A structured JSON response sent back to the client with an HTTP status
        code of 422 (Unprocessable Entity). The response contains:
        
        - `type`: A string indicating the nature of the error, in this case 
          set to `"about:blank"`, following the format used in some RESTful APIs.
        
        - `title`: A brief title describing the error, set to `"Validation Error"`.
        
        - `status`: The HTTP status code, set to `422`, indicating a validation error.

        - `detail`: A string message derived from the first error in the validation 
          exception (`exc`). It includes both the error message (`exc._errors[0]["msg"]`) 
          and the invalid data that caused the error (`exc._errors[0]["input"]`). This 
          provides clear feedback to the user about what went wrong.

        - `instance`: A string representing the URL of the request that caused the 
          validation error. This can be useful for debugging purposes.
    
    Example Response:
    ----------------
    When a validation error occurs, this handler sends a response like:
    
    {
        "type": "about:blank",
        "title": "Validation Error",
        "status": 422,
        "detail": "Error message here, got: Invalid input",
        "instance": "http://localhost/path/to/endpoint"
    }
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "type": "about:blank",
            "title": "Validation Error",
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "detail": f'{exc._errors[0]["msg"]}, got: {exc._errors[0]["input"]}',
            "instance": str(request.url),
        },
    )


@app.exception_handler(HTTPException)
async def validation_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse( 
        status_code=exc.status_code,
        content={
            "type": "about:blank",
            "title": "Request Error",
            "status": exc.status_code,
            "detail": exc.detail,
            "instance": str(request.url),
        }
    )
    



app.include_router(users.router)


