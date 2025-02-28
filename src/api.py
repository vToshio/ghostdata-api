from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from .helpers import generate_user
import asyncio

router = APIRouter()

@router.get('/users/')
async def users(rows:int, location:str='pt-BR'):
    '''
    Endpoint da API que retorna uma lista de usuários de acordo com a quantidade de registros(rows) passadas.

    Args:
    - rows (int): quantidade de registros de usuários gerados,
    - location (str): local de origem dos nomes, ruas, cidades, etc...

    Exemplo de uso:
    {url}/users?rows=15&location=en-US

    Retorno:
    {
        'status_code': 200,
        'users': {
            'id': ?,
            'first_name': ?,
            'last_name': ?,
            'email': ?,
            'phone_number': ?,
            'address': {
                'number': ?,
                'street_name': ?,
                'city': ?,
                'country': ?,
                'postal_code': ?,
            }
        }
    }
    '''
    try:
        response = await asyncio.to_thread(generate_user, rows, location)

        if response['status_code'] == 500:
            raise HTTPException(status_code=500, detail=response.description)

        return JSONResponse(response , status_code=200)
    except Exception as e:
        return JSONResponse({'description': str(e)}, status_code=500)