from fastapi import (
    APIRouter,
    HTTPException,
    Request,
    Query
)
from bson import json_util
from fastapi.responses import JSONResponse
from random import randint
from . import (models, const_pipeline)
import unicodedata
from typing import List, Optional
import json

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
    babynames = request.app.database["newNames"]

    pipeline = [
    {"$match": {"name": n}},
    {"$lookup": {
        "from": "newNames",
        "localField": "recommendedNames",
        "foreignField": "name",
        "as": "associedDetails"
    }},
    {"$project": {
        "_id": 1,
        "name": 1,
        "origin" : 1,
        "meaning" : 1,
        "similiarNames" : 1,
        "associedDetails":{
            "origin": 1,
            "meaning": 1,
            "name" : 1,
            "similiarNames" : 1,
            "_id" : 1
        }
    }}
]
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


@router.get('/phraseNames')
def get_phrase_names(request : Request, names : List[str] = Query(...)):
    try:
        db_names = request.app.database['names']
        response_array = []
        for n in names: 
            documento = db_names.aggregate(const_pipeline.pipeline(n))
            response_array.append([models.NameDetails(**doc) for doc in documento][0].__repr__())
        return JSONResponse(response_array)
            
        return response_array
    except Exception as e:
        return e