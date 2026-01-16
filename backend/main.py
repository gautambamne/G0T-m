from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
from app.config.settings import settings
from app.router import api_router
from app.advices.global_exception import GlobalExceptionHandler
from app.config.settings import settings


app = FastAPI(
    debug=settings.debug,
    title="Learn FastAPI",
    description="A simple project to learn FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
GlobalExceptionHandler.register_exception_handlers(app)

if __name__ == "__main__":
    import uvicorn
    print("Starting server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)




