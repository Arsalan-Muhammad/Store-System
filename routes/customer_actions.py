from email.policy import HTTP

from fastapi import Depends, FastAPI , HTTPException , status , APIRouter
from fastapi.routing import APIRoute
from pydantic import BaseModel
import schemas 
import models
from database import get_db
from sqlalchemy.orm import Session
import auth

class BuyItem(BaseModel):
    price : float
    quantity : int
router = APIRouter(tags=["Users-actions"])

@router.post("/buy-item/{name}")
def buy_item(name : str , buy : BuyItem , db : Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.name == name).first()

    if buy.quantity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Quantity Is 0 enter Quantity >= 1")
    
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Sorry The Product Is Not Available Right Now!")
    pr = round(product.price * buy.quantity, 2) #pyright:ignore
 
    
    if buy.price > pr: #pyright:ignore
        rp = buy.price - pr
        return {"Your Item" : product , "Remaining Money" : rp}
    
    return {"Your Item" : product}