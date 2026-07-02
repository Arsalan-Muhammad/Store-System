from fastapi import Depends, FastAPI , HTTPException , status , APIRouter , UploadFile , File , Form
from pydantic import Tag
import schemas 
import models
from database import get_db , engine
from sqlalchemy.orm import Session
import auth

router = APIRouter(tags=["Admin Actions"])

@router.post("/products")
async def add_product(
    name: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    quantity: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    image = await file.read()

    new_product = models.Products(
        name=name,
        price=price,
        category=category,
        quantity=quantity,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product
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
