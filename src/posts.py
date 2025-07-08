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
        db_phrases = request.app.database['phrases']
        documento = db_user.find_one({'userId' : user_token})

        # user_aux = db_user.find_one({'userId' : "9szypgwp9hwx415ckypm5m"})
        # new_user_phrases = user_aux['phrases']

        pprint.pprint(documento)
        pprint.pprint(type(documento))

        if not documento:

            # Capta as frases que possuem a assinatura do usuário (00000000000000000)
            new_user_phrases = []
            phrases = db_phrases.find({'assignature':  "00000000000000000"})
            for doc in phrases:
                # Adiciona as frases no usuário
                new_user_phrases.append(doc['Frase'])

            # If the user does not exist, create a new user with his atributes
            user = {'userId': user_token,
                    'phrases': [],
                    'assignature': "00000000000000000",
                    'phrases': new_user_phrases,
            }
            db_user.insert_one(user)

            print(user)
            return JSONResponse(json_util.dumps({'message' : 'New User Created'}), status_code=201)
        
        doc = UserResponse(**documento)
        return doc
        
    except Exception as e:
        print(e)


