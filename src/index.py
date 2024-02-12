from fastapi import FastAPI, Request
import time
from .gets import router as gets_router
from pymongo import MongoClient



app = FastAPI()
URI = "mongodb+srv://laraesquivel:babynames@babys.iuiuuvp.mongodb.net/"


app.mongodb_client = MongoClient(URI)
app.database = app.mongodb_client['babynames']  

app.include_router(gets_router)



