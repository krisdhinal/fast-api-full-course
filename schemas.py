from typing import List
from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    class Config():
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class LihatUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

    class Config():
        orm_mode = True


class LihatBlog(BaseModel):
    # untuk menghendel error ( value is not a valid dict (type=type_error.dict))
    title: str
    body: str
    creator: LihatUser

    class Config():
        orm_mode = True
