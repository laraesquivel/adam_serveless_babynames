from fastapi import FastAPI, Request
import time
from .gets import router as gets_router
from pymongo import MongoClient



app = FastAPI()
URI = "mongodb+srv://laraesquivel:babynames@babys.iuiuuvp.mongodb.net/"


#handler = Mangum(app)  # handler for deploy FastAPI to lambdas

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(URI)
    app.database = app.mongodb_client['babynames']

app.include_router(gets_router)



