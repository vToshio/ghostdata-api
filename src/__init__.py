from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from src.api import router

def create_app() -> FastAPI:
    '''
    Cria e configura uma instância de aplicação FastAPI
    '''
    app = FastAPI()
    
    app.include_router(router)
    
    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
    return app