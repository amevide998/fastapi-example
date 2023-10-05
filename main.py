from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Blog(BaseModel):
    id: int
    text: str
    
@app.post(path="/blog")
def create_blog(item: Blog):
    return {"data": item}

@app.get("/blog")
def index(limit = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {"data": f"blog list of {limit} published blog"}
    else:
        return {"data": f"blog list of {limit} blog"}


@app.get("/blog/unpublished")
def unpublished():
    return {"data": "unpublished blog"}


@app.get("/blog/{id}")
def show(id: int):
    return {"data": {"blogid": id}}


@app.get("/blog/{id}/comment")
def comments(id, limit=10):
    return {"data": {"1", "2"}}

#main
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
