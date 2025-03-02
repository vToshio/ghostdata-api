from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from .helpers import Generator
import asyncio

router = APIRouter()

@router.get('/user')
async def user(gender:str='any', safe:bool=True, location:str='pt-BR'):
    '''
    Endpoint da API que retorna os dados de um único usuário de acordo seu sexo.

    Args:
    - gender(str): define o sexo do usuário criado, sendo 'f', 'm', ou 'any'.
    - safe(bool): se o e-mail gerado é um e-mail não oficial ou não.
    - locale(str): define a localização de origem dos dados ('pt-BR', 'en-US', etc...)
    '''
    response = Generator.generate_user(gender, safe, location)    
    return JSONResponse(response, status_code=200)

@router.get('/users/')
async def users(rows:int, gender:str='any', safe:bool=True, location:str='pt-BR'):
    '''
    Endpoint da API que retorna uma lista de usuários de acordo com a quantidade de registros(rows) passadas.

    Args:
    - rows(int): define a quantidade de usuários que serão retornados.
    - gender(str): define o sexo do usuário criado, sendo 'f', 'm', ou 'any'.
    - safe(bool): se o e-mail gerado é um e-mail não oficial ou não.
    - locale(str): define a localização de origem dos dados ('pt-BR', 'en-US', etc...)
    '''
    response = await asyncio.to_thread(Generator.generate_users, rows, gender, safe, location)
    return JSONResponse(response , status_code=200)