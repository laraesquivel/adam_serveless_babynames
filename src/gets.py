from fastapi import (
    APIRouter,
    HTTPException,
    Request,
)
from bson import json_util
from fastapi.responses import JSONResponse
from random import randint
from . import (models, const_pipeline)
import unicodedata
from typing import List, Optional

router = APIRouter(tags=["gets"])


@router.get("/")
def root():
    return {"message": "Hello World"}


@router.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}"}



@router.get('/getNames')
def get_test(request : Request, name: str=None):
    if not name:
        raise HTTPException(status_code=400, detail="Por favor, forneça um nome para pesquisar na lista de nomes.")
    normalized_string = ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')

    n = normalized_string.capitalize()
    babynames = request.app.database["names"]

    pipeline = const_pipeline.pipeline(n)
    results = list(babynames.aggregate(pipeline))
    name_details = [models.NameDetails(**item) for item in results]
    response = name_details[0].__repr__()
    return JSONResponse(response)


@router.get("/getUser")
def get_rec_phrase(request : Request, userId : str = None):
    try:
        users_collection = request.app.database['users']
        parcial_response = users_collection.find_one({'userId':userId})
        if parcial_response:
             user = models.UserResponse(**parcial_response)
             return user
        raise Exception
    except Exception as e:
            return JSONResponse(json_util.dumps({'message':e}),status_code=500)
    return JSONResponse(json_util.dumps({'menssage':  "This HTTP triggered function executed successfully. Pass a userId in the query string or in the request body for a personalized response."}),
             status_code=400)


