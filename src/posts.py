from fastapi import (
    APIRouter,
    Request,
)

from bson import Timestamp, json_util
from fastapi.responses import JSONResponse
import datetime



router = APIRouter(tags=["posts"])


@router.post('/postAction')
def post_actions(request : Request) -> JSONResponse:
    date_hour = datetime.utcnow()
    timestamp = Timestamp(int(date_hour.timestamp()), 0)

    try:
        req_body = request.json()
        req_body['timestamp'] = timestamp

    except ValueError:
        return JSONResponse(json_util.dumps({"message" : "Invalid Req_Body"}, status_code=400))

    try:
        collection_actions = request.app.database['actions']


        result = collection_actions.insert_one(req_body)
        return JSONResponse(json_util.dumps({'message': 'Sucess in insert a new document','id' : str(result.inserted_id)}), status_code=201)

    except Exception as e:
        return JSONResponse(f"Error in insert a new document in collection: {str(e)}", status_code=500)
    

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