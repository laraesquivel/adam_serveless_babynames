from fastapi import (
    APIRouter,
    Request,
    HTTPException
)
from bson import Timestamp, json_util
from fastapi.responses import JSONResponse
from datetime import datetime
from .models import ActionRequest, User, UserResponse
from .const_pipeline import pipeline
from pymongo.collection import Collection
import pytz
from pymongo import errors, MongoClient
import os
from dotenv import load_dotenv
import pprint

load_dotenv()
URI = os.getenv('URI')

mongo_client = MongoClient(URI)
database = mongo_client['babynames']
collection_actions = database['actions']


router = APIRouter(tags=["posts"])

@router.post('/postAction')
def post_actions(request : Request, actions : ActionRequest):
    try:
        db = request.app.database['actions']
        nameDB = request.app.database['newNames']
        time = int(datetime.now(pytz.timezone("America/Bahia")).timestamp())
        item = actions.dict()
        pprint.pprint(1)
        item['timestamp'] = Timestamp(time,0)
        pprint.pprint(2)
        db.insert_one(item)
        return JSONResponse({'message' : 'Ok!'}, status_code=201)
                
    except Exception as e:
        pprint.pprint(e)
        return JSONResponse({"message" : 'canoot get db'}, status_code=503)
    
    #return JSONResponse({"message" : "Invalid Req_Body"}, status_code=400)
  

@router.post("/user")
def post_new_user(request: Request, user :User ) -> JSONResponse:

    try:
        user_token = user.userId
        db_user = request.app.database['users']
        documento = db_user.find_one({'userId' : user_token})

        pprint.pprint(documento)
        pprint.pprint(type(documento))

        if not documento:
            user = db_user.insert_one({'userId' : user_token})
            print(user)
            return JSONResponse(json_util.dumps({'message' : 'New User Created'}), status_code=201)
        
        doc = UserResponse(**documento)
        return doc
        
    except Exception as e:
        print(e)


