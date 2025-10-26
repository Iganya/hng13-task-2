from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from country import routes
from fastapi.exceptions import RequestValidationError
from db import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  # Or another status code
        content={"error": "Validation failed"},
        )
app.include_router(routes.router)
