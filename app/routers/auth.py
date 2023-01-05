from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from .. import database,schemas,models,utils,oauth2
from . import user

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: schemas.UserLogin,db: Session = Depends(database.get_db)):
    #find the user with the email
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    #check password match the one in the datbase
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    #create a token and return token

    access_token = oauth2.create_access_token(data={"user_id":user.id})#put infos u want to encoded into the token
    return {"access_token":access_token, "token_type":"bearer"}