from fastapi import Depends, FastAPI , HTTPException , status
import schemas 
import models
from database import get_db , engine
from sqlalchemy.orm import Session
app = FastAPI()

models.Base.metadata.create_all(bind=engine)
@app.get("/")
def home():
    return {"Hi!" : "Welcome to Arsalan Cosmetics Store!"}

@app.post("/add-product", status_code=status.HTTP_201_CREATED)
def add_product(
    product: schemas.CreateProduct,
    db: Session = Depends(get_db)
):

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