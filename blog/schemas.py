from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    description: str
    
class ShowBlog(Blog):
    title: str
    class Config():
        orm_mode = True
        
class User(BaseModel):
    username: str
    email: str
    password: str
    
class ShowUser(BaseModel):
    username: str
    email: str 
