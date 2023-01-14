from random import randrange
from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import sys
from . import models
from .database import engine,get_db
import time
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

get_db()
class Post(BaseModel):
    title: str
    content: str
    published:bool = True

while True:

    try:
        conn = psycopg2.connect(
        host='localhost', 
        user='postgres', 
        password='G0t0hell',
        database='fastapi',
        cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database is connected Successfully")
        break

    except:
        print("Error: ", sys.exc_info())
        time.sleep(2)


def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p


def find_index_post(id):
    for i , p in enumerate(my_posts):
        if p['id'] ==id :
            return i

my_posts = []

@app.get("/")
def login():
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return{"posts":posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # Direct from PostGres
    # cursor.execute("""SELECT   * FROM posts""")
    # posts =cursor.fetchall()
    # return {"data":posts}
    posts = db.query(models.Post).all()
    return{"posts":posts}




@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post,db: Session = Depends(get_db)):
    # post_dict =post.dict()
    # post_dict['id'] = randrange(0,1000000)
    # my_posts.append(post_dict)
    # return {"data":post_dict}
    #title str, content str
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    # (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"new post":new_post}

    # inefficient way
    new_post = models.Post(title = post.title,content = post.content,published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"new post":new_post}



   
@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute("""SELECT   * FROM posts WHERE id = %s""",(str(id)))
    post =cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post doesnot found")
    return {"post_detail":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    #deleting post
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post doesnot exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} doesnot exist")
    
    return{"data":updated_post}