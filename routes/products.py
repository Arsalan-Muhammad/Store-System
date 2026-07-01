from fastapi import Depends, FastAPI , HTTPException , status , APIRouter
from pydantic import Tag
import schemas 
import models
from database import get_db , engine
from sqlalchemy.orm import Session
import auth

router = APIRouter(tags=["Admin Actions"])
@router.post("/products", status_code=status.HTTP_201_CREATED)
def add_product(

    product: schemas.CreateProduct,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    user = db.query(models.Users).filter(
    models.Users.id == current_user.id
).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if user.role != "Admin": #pyright:ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You Are Not The Admin To Perform This Action"
            )
    
    existing_product = db.query(models.Products).filter(
        models.Products.name == product.name
    ).first()

    if existing_product:
        existing_product.quantity += product.quantity #pyright:ignore

        db.commit()
        db.refresh(existing_product)

        return {
            "message": "Product quantity updated",
            "product": existing_product
        }

    new_product = models.Products(**product.dict())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "New product added",
        "product": new_product
    }

@router.put("/products/{id}")
def update(
    UpdatedProduct: schemas.updateproduct , 
    id: int , 
    db : Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    updated_product = models.Products(**UpdatedProduct.dict())

    product = db.query(models.Products).filter(models.Products.id == id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = f"Product With id : {id} does not exists")

    product.price = updated_product.price
    product.quantity = updated_product.quantity

    return {"updated_product" : product}
