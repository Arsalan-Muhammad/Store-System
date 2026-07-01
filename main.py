
from fastapi import Depends, FastAPI , HTTPException , status
import auth
import schemas 
import models
from routes import products , customer_actions , auths , Normal_actions , users
from database import get_db , engine
app = FastAPI()

models.Base.metadata.create_all(bind=engine)
@app.get("/")
def home():
    return {"Hi!" : "Welcome to Arsalan Cosmetics Store!"}

app.include_router(products.router)
app.include_router(auths.router)
app.include_router(customer_actions.router)
app.include_router(Normal_actions.router)
app.include_router(users.router)
