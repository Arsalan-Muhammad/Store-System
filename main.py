
from fastapi import Depends, FastAPI , HTTPException , status
import schemas 
import models
from routes import products
from database import get_db , engine
app = FastAPI()

models.Base.metadata.create_all(bind=engine)
@app.get("/")
def home():
    return {"Hi!" : "Welcome to Arsalan Cosmetics Store!"}

app.include_router(products.router)

