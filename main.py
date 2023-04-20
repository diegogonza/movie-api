from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
import movies #listado de las películas
from pydantic import BaseModel, Field
from typing import Optional
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title = 'Movie App'
app.version = '0.0.1'

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
    id: Optional[int] = None
    title: str
    overview: str
    year: int
    rating: float = Field(ge= 1, le= 5.0) #ge = mayor o igual, le = menor o igual
    category: str
    class Config:
        schema_extra = {
            'example': {
                'id': 0,
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
@app.get('/movies', tags=['movies'], status_code= 200, dependencies=[Depends(JWTBearer)])
def get_movies():
    return JSONResponse(status_code= 200, content= movies.list_of_movies)

# Obtener lista de películas por ID
@app.get('/movies/{id}', tags=['movies'], status_code= 200)
def get_movie(id: int):
    for item in movies.list_of_movies:
        if item['id'] == id:
            return JSONResponse(content= item)
        else: 
           return JSONResponse(status_code= 404, content= {'Messega' : 'ERROR: Recurso no encontrado'})

# Obtener lista de películas por CATEGORÍA
@app.get('/movies/', tags=['movies'], status_code= 200)
def get_movies_by_category(category: str):
    movies_by_category = [item for item in movies.list_of_movies if item['category'] == category] 
            
    return JSONResponse(status_code= 200, content= movies_by_category)

# Crea una películas
@app.post('/movies', tags=['movies'], status_code= 201)
def create_movie(movie: Movie):
    movies.list_of_movies.append(movie)
    return JSONResponse(status_code= 201, content= {'message': 'Su película ha sido creada'})

# Modificación de películas por ID
@app.put('/movies/{id}', tags=['movies'])
def edit_movie(id: int, movie: Movie):
    for item in movies.list_of_movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            
            return JSONResponse(content= {'message': 'Su película ha sido modificada'})
        
# Eliminación de película por ID
@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    for item in movies.list_of_movies:
        if item['id'] == id:
            movies.list_of_movies.remove(item)            
            
            return JSONResponse(content= {'message': 'Su película ha sido Eliminada'})