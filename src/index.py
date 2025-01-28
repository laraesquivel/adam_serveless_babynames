from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .gets import router as gets_router
from .posts import router as posts_router
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
URI = os.getenv('URI')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://babynames-seven.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mongodb_client = MongoClient(URI)
app.database = app.mongodb_client['babynames']  

app.include_router(gets_router)
app.include_router(posts_router)



