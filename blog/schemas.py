from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    description: str
    
class ShowBlog(BaseModel):
    title: str
    class Config():
        from_attributes = True
        
class User(BaseModel):
    username: str
    email: str
    password: str
    
class ShowUser(BaseModel):
    username: str
    email: str 
    class Config():
        from_attributes = True
