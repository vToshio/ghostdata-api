from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get('/users/')
def users():
    return JSONResponse({'Hello': 'Ghost!'}, status_code=200)