from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
)

from bson import Timestamp, json_util
from fastapi.responses import JSONResponse



router = APIRouter(tags=["gets"])


@router.get("/")
def root():
    return {"message": "Hello World"}


@router.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}"}

@router.get("/getNames/{name}")
def get_names(request: Request, name: str = None):
    # Send a ping to confirm a successful connection
    if not name:
        raise HTTPException(status_code=400, detail="Por favor, forneça um nome para pesquisar na lista de nomes.")
    if name:
        babynames = request.app.database["names"]
        print(babynames)
        result = json_util.dumps(babynames.find_one({'name': name}), default = str)
        if result:
            print(result)
            return JSONResponse(content=result, status_code=200, media_type="application/json")
        result = json_util.dumps(babynames.find_one({'closers' : name}))
        if result:
            return JSONResponse(content=result,status_code=200, media_type="application/json")
        

    return JSONResponse(content=json_util.dumps({'error' : "Não encontrado!"}), status_code=404, media_type="application/json")

@router.get("/getRecPhrase/userId")
def get_rec_phrase(request : Request, userId : str = None):
    pass

@router.get("getNamesToPhrase/phrase")
def get_names_to_phrase(request : Request, phrase : str = None):
    pass