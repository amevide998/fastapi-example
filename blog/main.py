from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, LocalSession
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
        
@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, description=request.description)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog')
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}')
def getById(id, db: Session = Depends(get_db), response: Response = 200):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail' : f'blog with id {id} not found'}
    return blog