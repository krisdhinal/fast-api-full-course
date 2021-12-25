from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


class LihatBlog(BaseModel):
    # untuk menghendel error ( value is not a valid dict (type=type_error.dict))
    title: str
    body: str

    class Config():
        orm_mode = True
