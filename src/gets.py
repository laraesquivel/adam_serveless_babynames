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
from pydantic import parse_obj_as
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

@router.get("/getRecPhrase/{user_id}")
def get_rec_phrase(request : Request, user_id : str = None):
    try:
        users_collection = request.app.database['users']
        phrases_collection = request.app.database['phrases']
        parcial_response = users_collection.find_one({'tokenId':user_id})
        if user_id and 'nextPhrases' in parcial_response:
            arr_phrases = parcial_response['nextPhrases']
            if arr_phrases:
                random_index = randint(0,len(arr_phrases) - 1)
                response = json_util.dumps({'phrase' : arr_phrases[random_index], 'message': 'Its all okay'})
                return JSONResponse(response, status_code=200)
        randon_phrase = json_util.dumps(phrases_collection.aggregate([{"$sample":{"size":1}}]).next())
        return JSONResponse(randon_phrase,status_code=200,mimetype="application/json")

    except Exception as e:
            return JSONResponse(json_util.dumps({'message':e}),status_code=500)
    return JSONResponse(json_util.dumps({'menssage':  "This HTTP triggered function executed successfully. Pass a userId in the query string or in the request body for a personalized response."}),
             status_code=400)


@router.get("getNamesToPhrase/{phrase}")
def get_names_to_phrase(request : Request, phrase : str = None):
    if phrase:
        try:
            phrases_collection = request.app.database['phrase']
            response = phrases_collection.find_one({'phrase':phrase})
            return JSONResponse(content=json_util.dumps(response), status_code=200, media_type="application/json")
            
        except Exception as e:
            return JSONResponse(json_util.dumps({'message':'Some error ocurred!'}),status_code=500)
    return JSONResponse(json_util.dumps({'message':'Bad Request, phrase is missing!'}),status_code=400)