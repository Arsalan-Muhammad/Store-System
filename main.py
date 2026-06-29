from math import prod
from multiprocessing import synchronize

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

@app.get("/get-product/{id}")
def get_product(id: int , db : Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.id == id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Cannot Find Product with id : {id}")
    
    return product

@app.get("/get-all-products")
def all_products(db : Session = Depends(get_db)):
    products = db.query(models.Products).all()

    if not products:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT , detail="No Product Found")
    
    return products

@app.put("/edit-product/{id}")
def update(UpdatedProduct: schemas.updateproduct , id: int , db : Session = Depends(get_db)):
    updated_product = models.Products(**UpdatedProduct.dict())

    product = db.query(models.Products).filter(models.Products.id == id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = f"Product With id : {id} does not exists")

    product.price = updated_product.price
    product.quantity = updated_product.quantity

    return {"updated_product" : product}
