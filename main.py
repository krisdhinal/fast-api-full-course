# for make object into list or array
from typing import List
# fast api liblary for better microservices
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.sql.functions import user
# model schema from schemas file
import schemas
# model and table
import models
# seeting file for connecting table to sqlite
from database import SessionLocal, engine
# liblary for query sql leanguage
from sqlalchemy.orm import Session
# hashing class for encrypt password
from hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)

# getting database


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Blogs Route


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
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


# Users Route

@app.post('/user', response_model=schemas.LihatUser, tags=["Users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# @app.get('/user', response_model=List[schemas.LihatUser], tags=["Users"])
# def get_all_user(db: Session = Depends(get_db)):
#     users = db.query(models.User).all()
#     return users


@app.get('/user/{id}', status_code=200, response_model=schemas.LihatUser, tags=["Users"])
def show_user_by_id(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with id {id} not found'}
    return user


# @app.put('/user/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["Users"])
# def update_user(id, request: schemas.User, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id)
#     if not user.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"User with id {id} not found")
#     user.update(request.dict())
#     db.commit()
#     return {f"the user with id {id} successfully updated"}


# @app.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
# def delete_blog(id, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id)
#     if not user.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"User with id {id} not found")
#     user.delete(synchronize_session=False)
#     db.commit()
#     return {f"the user with id {id} successfully deleted"}
