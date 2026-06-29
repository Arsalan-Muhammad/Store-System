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
    post = db.query(models.Products).filter(models.Products.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Cannot Find Product with id : {id}")
    
    return post