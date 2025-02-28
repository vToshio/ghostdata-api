from fastapi import FastAPI
from src.api import router

def create_app() -> FastAPI:
    '''
    Create and configure a FastAPI App instance
    '''
    app = FastAPI()
    app.include_router(router)
    return app