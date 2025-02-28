from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from src.api import router

def create_app() -> FastAPI:
    '''
    Cria e configura uma instância de aplicação FastAPI
    '''
    app = FastAPI()
    app.include_router(router)
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    return app