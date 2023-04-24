from models.movie import Movie as MovieModel
from schemas.movie import Movie

class MovieServices():
    def __init__(self, db) -> None:
        self.db = db
        
    # Obtener lista de películas
    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result
    
    # Obtener lista de películas por ID
    def get_movie_by_id(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    # Obtener lista de películas por CATEGORÍA
    def get_movies_by_category(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
    
    # Crea una películas   
    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return
    
    # Modificación de películas por ID
    def update_movie(self, id: int, data: Movie):
        movie = self.get_movie_by_id(id)
        
        movie.title = data.title
        movie.overview = data.overview
        movie.year = data.year
        movie.rating = data.rating
        movie.category = data.category

        self.db.commit()        
        return
    
    # Eliminación de película por ID
    def delete_movie(self, id: int):
        movie_to_delete = self.get_movie_by_id(id)
        self.db.delete(movie_to_delete)
        self.db.commit()        
        return