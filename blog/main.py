from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models, hashing
from .database import engine, LocalSession
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
        
@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blog'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, description=request.description)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', response_model=List[schemas.ShowBlog],tags=['blog'])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog,tags=['blog'])
def getById(id, db: Session = Depends(get_db), response: Response = 200):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail' : f'blog with id {id} not found'}
    return blog


@app.delete(path='/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blog'])
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {'detail': f'blog with id {id} deleted'}

@app.put(path='/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
    blog.update({'title': request.title, 'description': request.description})
    db.commit()
    return {'detail': f'blog with id {id} updated'}


# USER 
@app.post(path='/user', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=['user'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(username=request.username, email=request.email, password=hashing.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['user'])
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} not found')
    return user
    