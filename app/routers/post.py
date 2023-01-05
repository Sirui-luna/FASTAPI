
from .. import models, schemas
from fastapi import FastAPI, Depends,Response, status, HTTPException,APIRouter
import time
from sqlalchemy.orm import Session
from ..database import engine, get_db
from typing import Optional, List

router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)

@router.get("/",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
   #auto convert the the post request to dictionary, e.g. title = post.title, content=post.content
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    #retrieve the new post and store the value to the new_post
    db.refresh(new_post)
    return new_post
#method 1 - no predefined format
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return{"message": "successfully create a post"}

#method 2: use pre-defined Item model (auto validation)
#SQL way
# def create_posts1(item: Item):
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING * """,(item.title,item.content, item.published)) #order matters
    # new_post = cursor.fetchone()
    # conn.commit()
    # return{"data": new_post}



#specify which post you wanna get

@router.get("/{id}", response_model=schemas.Post)
#can auto convert it to interger
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts WHERE id = %s""",(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    #post = find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return post

#delete post

#find the index of the post in the list that has the specified id

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
     
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    post.delete(synchronize_session=False)
    db.commit()

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content= %s, published=%s WHERE id= %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    #just the query
    post_query = db.query(models.Post).filter(models.Post.id == id)
    #the post, find the first post that match the id
    post = post_query.first()  # type: ignore
    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    #convert json to dictionary
    post_query.update(updated_post.dict(), synchronize_session=False)  # type: ignore
    db.commit()
    return post_query.first()