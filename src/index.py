from fastapi import FastAPI, Request
import time
from .gets import router as gets_router
from .posts import router as posts_router
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
URI = os.getenv('URI')


app.mongodb_client = MongoClient(URI)
app.database = app.mongodb_client['babynames']  

app.include_router(gets_router)
app.include_router()



