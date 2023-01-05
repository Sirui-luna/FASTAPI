from typing import Optional, List
from urllib import response
from fastapi import FastAPI, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from fastapi import Response, status, HTTPException
import psycopg2
from . import utils
# to get column name
from psycopg2.extras import RealDictCursor
import time
#sqlalchemy
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post,user,auth
#sqlalchemy
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

#import all routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

#decorate?
#send an get request to the api (HTTP methods)
# app.get("[path]")
# order matters: fastapi will only look at the first matching function, so if there are two functions with the same name, only the first one will run.
@app.get("/")

#api functions
# add async at the front if you want a function perform asyncrohnisely
def root():
    return {"message": "Hello World!"}
# convert messages to json and send back to user

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id":1},{"title": "title of post 2", "content": "content of post 2", "id":2}]

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

#connect to database
#psycopg2 is the default driver of pgsql
while True:# keep looping until we are able to connect to the database
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='abc123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection was successful")
        break
    except Exception as error:
        print("database connection was failed")
        print("Error: ", error)
        #if fail to connect then try again every 2 seconds
        time.sleep(2)


#specify which post you wanna get

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

#ORDER matters, otherwise fastapi will look at the get(post/get/{id}) first
# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail": post}


