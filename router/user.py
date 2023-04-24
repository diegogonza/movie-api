from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.jwt_manager import create_token

user_router = APIRouter()

class User(BaseModel):
    email: str
    password: str
    

@user_router.post('/login', tags=['Auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == '123':
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content= token)
    else:
        return JSONResponse(status_code=200, content= {'message': 'Usuario invalido'})