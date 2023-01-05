from pydantic import BaseModel, EmailStr
from datetime import datetime
#Schema

class PostBase(BaseModel):
    title: str
    content: str
    #the default value set to true, if the user doesn't provide the info
    published: bool = True

class PostCreate(PostBase):
    #inheret all the attributes in PostBase schema
    pass


class Post(PostBase):
    #title, content and published are inhereted from PostBase schema
    id: int
    created_at: datetime
    #tell pydantic to ignore that it is not a dictionary
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

#respond for user creation
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


