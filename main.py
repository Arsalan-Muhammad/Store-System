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

@app.post("/add-product")
def add_product(product:schemas.CreateProduct , db : Session = Depends(get_db)):
    new_product = models.Products(**product.dict())
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
