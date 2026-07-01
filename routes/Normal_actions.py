from fastapi import Depends, FastAPI , HTTPException , status , APIRouter
from fastapi.routing import APIRoute
from pydantic import BaseModel
import schemas 
import models
from database import get_db
from sqlalchemy.orm import Session
import auth

router = APIRouter(tags=["Actions For Both Admin And Customers"])
@router.get("/products/{id}")
def get_product(
    id: int, 
    product: schemas.CreateProduct,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
    ):
    product = db.query(models.Products).filter(models.Products.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Cannot Find Product with id : {id}")
    
    return product

@router.get("/products")
def all_products(
    db : Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)              
):
    products = db.query(models.Products).all()

    if not products:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT , detail="No Product Found")
    
    return products