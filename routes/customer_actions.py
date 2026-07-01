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

@router.get("buy-item/{name}")
def buy_item(name : str , buy : BuyItem , db : Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.name == name).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Sorry The Product Is Not Available Right Now!")
    
    if buy.price < product.price: #pyright:ignore
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE , detail="The price given by you is not Acceptable")
    
    if buy.price > product.price: #pyright:ignore
        rp = product.price - buy.price
        return {"Your Item" : product , "Remaining Money" : rp}
    
    return {"Your Item" : product}