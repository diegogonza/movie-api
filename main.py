from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()
app.title = 'Movie App'
app.version = '0.0.2'

Base.metadata.create_all(bind = engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] == 'admin@gmail.com':
            raise HTTPException(status_code= 403, detail='Credenciales invalidas')
        
class User(BaseModel):
    email: str
    password: str
    
class Movie(BaseModel):
    title: str
    overview: str
    year: int
    rating: float = Field(ge= 1, le= 5.0) #ge = mayor o igual, le = menor o igual
    category: str
    class Config:
        schema_extra = {
            'example': {
                'title': 'My title',
                'overview': 'Description',
                'year': 2023,
                'rating': 5.0,
                'category': 'Acción'
            }
        }
    
    
@app.get('/', tags=['Home'])
def message():
    return {'<h1>Hola</h1>'}

@app.post('/login', tags=['Auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == '123':
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content= token)
    else:
        return JSONResponse(status_code=200, content= {'message': 'Usuario invalido'})

# Obtener lista de películas
@app.get('/movies', tags=['movies'], status_code= 200)
def get_movies():
    db = Session()
    results = db.query(MovieModel).all()
    return JSONResponse(status_code= 200, content= jsonable_encoder(results))

# Obtener lista de películas por ID
@app.get('/movies/{id}', tags=['movies'], status_code= 200)
def get_movie(id: int):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    
    if not result:
        return JSONResponse(status_code= 404, content= {'Messega' : 'ERROR: Recurso no encontrado'})
 
    return JSONResponse(status_code= 200, content= jsonable_encoder(result))

# Obtener lista de películas por CATEGORÍA
@app.get('/movies/', tags=['movies'], status_code= 200)
def get_movies_by_category(category: str):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    
    if not result:
        return JSONResponse(status_code= 404, content= {'Messega' : 'ERROR: Recurso no encontrado'})

    return JSONResponse(status_code= 200, content= jsonable_encoder(result))

# Crea una películas
@app.post('/movies', tags=['movies'], status_code= 201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code= 201, content= {'message': 'Su película ha sido creada'})

# Modificación de películas por ID
@app.put('/movies/{id}', tags=['movies'])
def edit_movie(id: int, movie: Movie):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    
    if not result:
        return JSONResponse(status_code= 404, content= {'Messega' : 'ERROR: Recurso no encontrado'})

    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
            
    return JSONResponse(content= {'message': 'Su película ha sido modificada'})
        
# Eliminación de película por ID
@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    
    if not result:
        return JSONResponse(status_code= 404, content= {'Messega' : 'ERROR: Recurso no encontrado'})
    
    db.delete(result)
    db.commit()

    return JSONResponse(content= {'message': 'Su película ha sido Eliminada'})