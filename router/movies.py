from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from services.movie import MovieServices
from schemas.movie import Movie

movies_router = APIRouter() 

# Obtener lista de películas
@movies_router.get('/movies', tags=['movies'], status_code= 200)
def get_movies():
    db = Session()
    results = MovieServices(db).get_movies()
    return JSONResponse(status_code= 200, content= jsonable_encoder(results))

# Obtener lista de películas por ID
@movies_router.get('/movies/{id}', tags=['movies'], status_code= 200)
def get_movie_by_id(id: int):
    db = Session()
    result = MovieServices(db).get_movie_by_id(id)
    
    if not result:
        return JSONResponse(status_code= 404, content= {'Messega' : 'ERROR: Recurso no encontrado'})
 
    return JSONResponse(status_code= 200, content= jsonable_encoder(result))

# Obtener lista de películas por CATEGORÍA
@movies_router.get('/movies/', tags=['movies'], status_code= 200)
def get_movies_by_category(category: str):
    db = Session()
    result = MovieServices(db).get_movies_by_category(category)
    
    if not result:
        return JSONResponse(status_code= 404, content= {'Messega' : 'ERROR: Recurso no encontrado'})

    return JSONResponse(status_code= 200, content= jsonable_encoder(result))

# Crea una películas
@movies_router.post('/movies', tags=['movies'], status_code= 201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieServices(db).create_movie(movie)
    return JSONResponse(status_code= 201, content= {'message': 'Su película ha sido creada'})

# Modificación de películas por ID
@movies_router.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieServices(db).get_movie_by_id(id)
    
    if not result:
        return JSONResponse(status_code= 404, content= {'Messega' : 'ERROR: Recurso no encontrado'})

    MovieServices(db).update_movie(id, movie)     
    return JSONResponse(content= {'message': 'Su película ha sido modificada'})
        
# Eliminación de película por ID
@movies_router.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    db = Session()
    result = MovieServices(db).get_movie_by_id(id)
    
    if not result:
        return JSONResponse(status_code= 404, content= {'Messega' : 'ERROR: Recurso no encontrado'})
    
    MovieServices(db).delete_movie(id)
    return JSONResponse(content= {'message': 'Su película ha sido Eliminada'})