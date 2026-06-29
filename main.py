from fastapi import Depends, FastAPI , HTTPException , status
from . import schemas , database
from . import models
from . database import get_db
from sqlalchemy.orm import Session
app = FastAPI()

@app.get("/")
def home():
    return {"Hi!" : "Welcome to Arsalan Cosmetics Store!"}

@app.post("/add-product/{name}/{category}")
def add_product(name : str , category : str ,  product:schemas.CreateProduct , db : Session = Depends(get_db)):
    new_product = models.Products(**product.dict())
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
