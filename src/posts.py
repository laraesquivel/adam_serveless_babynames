from fastapi import (
    APIRouter,
    Request,
    HTTPException
)

from bson import Timestamp, json_util
from fastapi.responses import JSONResponse
from datetime import datetime
from . import models
from pymongo.collection import Collection


router = APIRouter(tags=["posts"])


@router.post('/postAction', response_model=models.ActionResult)
async def post_actions(request: Request, action_request: models.ActionRequest) -> JSONResponse:
    try:
        date_hour = datetime.utcnow()
        timestamp = Timestamp(int(date_hour.timestamp()), 0)

        # Adiciona o timestamp ao objeto Pydantic
        action_request.timestamp = timestamp

        # Convertendo o objeto Pydantic para um dicionário
        req_body = action_request.dict()

        collection_actions: Collection = request.app.database['actions']
        result = collection_actions.insert_one(req_body)

        return models.ActionResult(message='Sucesso na inserção de um novo documento', id=str(result.inserted_id))

    except ValueError:
        raise HTTPException(status_code=400, detail="Corpo da requisição inválido")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir um novo documento na coleção: {str(e)}")

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