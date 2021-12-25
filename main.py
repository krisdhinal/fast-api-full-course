# for make object into list or array
from typing import List
# fast api liblary for better microservices
from fastapi import FastAPI, Depends, HTTPException, status
# model schema from schemas file
import schemas
# model and table
import models
# seeting file for connecting table to sqlite
from database import SessionLocal, engine
# liblary for query sql leanguage
from sqlalchemy.orm import Session, session

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', response_model=List[schemas.LihatBlog], tags=["Blogs"])
def get_all_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=200, response_model=schemas.LihatBlog, tags=["Blogs"])
def show(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with id {id} not found'}
    return blog


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["Blogs"])
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    blog.update(request.dict())
    db.commit()
    return {f"the blog with id {id} successfully updated"}


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Blogs"])
def delete_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {f"the blog with id {id} successfully deleted"}


@app.post('/user', tags=["Users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name, email=request.email, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
