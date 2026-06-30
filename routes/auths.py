from fastapi import Depends , responses , status , HTTPException , APIRouter
from sqlalchemy.orm import Session
from .. import database , schemas , models , auth
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login(user_credentials:OAuth2PasswordRequestForm = Depends() , db : Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Invalid Credentials")
    
    if user.password != user_credentials.password: #pyright:ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Invalid Credentials")
    
    access_token = auth.create_access_token({"user_id" : user.id})

