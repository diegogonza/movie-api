from fastapi import FastAPI, Body
import movies


app = FastAPI()
app.title = 'Movie App'
app.version = '0.0.1'


@app.get('/', tags=['Home'])
def message():
    return {"Hola"}

@app.get('/movies', tags=['movies'])
def get_movies():
    return movies.list_of_movies

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
    for item in movies.list_of_movies:
        if item['id'] == id:
            return item
    return []

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str):
    movies_by_category = [item for item in movies.list_of_movies if item['category'] == category] 
    
    # movies_by_category = []
    # for item in movies.list_of_movies:
    #     if item['category'] == category:        
    #         movies_by_category.append(item)
            
    return movies_by_category

@app.post('/movies', tags=['movies'])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    movies.list_of_movies.append(
        {
            'id': id,
            'title': title,
            'overview': overview,
            'year': year,
            'rating': rating,
            'category': category  
        }
    )
    return movies.list_of_movies

@app.put('/movies/{id}', tags=['movies'])
def edit_movie(id: int, title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    for item in movies.list_of_movies:
        if item['id'] == id:
            item['title'] = title
            item['overview'] = overview
            item['year'] = year
            item['rating'] = rating
            item['category'] = category
            
            return movies.list_of_movies
        
@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    for item in movies.list_of_movies:
        if item['id'] == id:
            movies.list_of_movies.remove(item)            
            
            return movies.list_of_movies
