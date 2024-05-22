from fastapi import (
    APIRouter,
    Request,
    HTTPException
)

from bson import Timestamp, json_util
from fastapi.responses import JSONResponse
from datetime import datetime
from .models import ActionRequest, NamesRequest, NameInfo, NameData
from pymongo.collection import Collection
from pymongo import errors, MongoClient
import os
from dotenv import load_dotenv


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
        nameDB = request.app.database['names']
        item = actions.__repr__()
        documento = nameDB.find_one({'name': item['item']})

        if documento:
            item['itemID'] = documento['_id']
            db.insert_one(item)
            return JSONResponse({'message' : 'Ok!'}, status_code=201)
        
        
        db.insert_one(item)

        return JSONResponse({'message' : 'We dont have this name Id'},status_code=202)
        ''' 
           if db:
                try:
                    db.insert(item)
                    return  JSONResponse({"message" : "Ok!"} , status_code=201)
                except Exception as e:
                    return JSONResponse({"message":"Não conseguimos inserir isso!"},status_code=500)
            
            #return JSONResponse({'ok':item},status_code=201)'''
        
    except Exception as e:
        return JSONResponse({"message" : 'canoot get db'}, status_code=503)
    
    #return JSONResponse({"message" : "Invalid Req_Body"}, status_code=400)
  

@router.post("postNewUser")
def post_new_user(request: Request) -> JSONResponse:
    user_id = None
    date_hour = datetime.utcnow()
    timestamp = Timestamp(int(date_hour.timestamp()), 0)
    try:
        req_body = request.json()
        user_id = req_body['userId']

    except (ValueError, KeyError):
        return JSONResponse(json_util.dumps({"message":"Invalid Req_Body or missing 'userId'"}), status_code=400)

    if user_id:
        try:
            users_collection = request.app.database['users']
            result = users_collection.insert_one({'tokenId': user_id, 'timestamp': timestamp})
            return JSONResponse(json_util.dumps({'message': 'Add new user', 'userId': str(result.inserted_id)}),
                                     status_code=201, mimetype="application/json")
        except Exception as e:
            return JSONResponse(json_util.dumps({'error': str(e)}), status_code=500, mimetype="application/json")
    
    return JSONResponse(json_util.dumps({'message': 'Bad Request, userId is missing!'}), status_code=400, mimetype="application/json")