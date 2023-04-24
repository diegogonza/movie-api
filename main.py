from fastapi import FastAPI, HTTPException, Request
from utils.jwt_manager import validate_token
from fastapi.security import HTTPBearer
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from router.movies import movies_router

app = FastAPI()
app.title = 'Movie App'
app.version = '0.0.2'

app.add_middleware(ErrorHandler)
app.include_router(movies_router)

Base.metadata.create_all(bind = engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] == 'admin@gmail.com':
            raise HTTPException(status_code= 403, detail='Credenciales invalidas')
 
@app.get('/', tags=['Home'])
def message():
    return {'<h1>Hola</h1>'}
