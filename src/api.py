from fastapi import APIRouter
from src.generators.user_generator import UserGenerator
from src.schemas.user_schemas import UserSchema
from typing import List

router = APIRouter()

@router.get('/user', response_model=UserSchema)
async def user(gender:str='any', safe:bool=True, location:str='pt-BR'):
    '''
    Endpoint da API que retorna os dados de um único usuário de acordo seu sexo.

    Args:
    - gender(str): define o sexo do usuário criado, sendo 'f', 'm', ou 'any'.
    - safe(bool): se o e-mail gerado é um e-mail não oficial ou não.
    - locale(str): define a localização de origem dos dados ('pt-BR', 'en-US', etc...)
    '''
    response = await UserGenerator.generate_one(gender, safe, location)    
    return response

@router.get('/users/', response_model=List[UserSchema])
async def users(rows:int, gender:str='any', safe:bool=True, location:str='pt-BR'):
    '''
    Endpoint da API que retorna uma lista de usuários de acordo com a quantidade de registros(rows) passadas.

    Args:
    - rows(int): define a quantidade de usuários que serão retornados.
    - gender(str): define o sexo do usuário criado, sendo 'f', 'm', ou 'any'.
    - safe(bool): se o e-mail gerado é um e-mail não oficial ou não.
    - locale(str): define a localização de origem dos dados ('pt-BR', 'en-US', etc...)
    '''
    response = await UserGenerator.generate_many(rows, gender, safe, location)
    return response