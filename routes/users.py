from fastapi import FastAPI, HTTPException, status, Depends , APIRouter
from sqlalchemy.orm import Session
import schemas , models , ultis
from database import get_db
router = APIRouter(
    tags=['Users']
)

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    hashed_password = ultis.hash_password(user.password)

    user_data = user.dict()
    user_data["password"] = hashed_password

    new_user = models.Users(**user_data)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user