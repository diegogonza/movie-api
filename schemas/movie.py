from pydantic import BaseModel, Field

class Movie(BaseModel): #schema
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
   