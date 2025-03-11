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
import logging
from collections import defaultdict
from itertools import groupby

router = APIRouter(tags=["gets"])

logging.basicConfig(level=logging.DEBUG)

@router.get("/")
def root():
    return {"message": "Hello World"}


@router.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}"}



@router.get('/getNames')
def get_test(request : Request, name: str=None):
    try:
        if not name:
            raise HTTPException(status_code=400, detail="Por favor, forneça um nome para pesquisar na lista de nomes.")
        normalized_string = ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')

        n = normalized_string.capitalize()
        babynames = request.app.database["newNames"]

        print(f"Recebendo requisição para: {name}")

        pipeline = const_pipeline.pipeline(n)
        results = list(babynames.aggregate(pipeline))

        print(f"Resultados do banco: {results}")

        name_details = [models.NameDetails(**item) for item in results]
        response = name_details[0].__repr__()
        return JSONResponse(response)
    
    except Exception as e:
        print(f"Erro no banco: {e}")
        return JSONResponse(json_util.dumps({'message':e}),status_code=500)


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
        db_names = request.app.database['newNames']
        response_array = []
        for n in names: 
            documento = db_names.aggregate(const_pipeline.pipeline(n))
            response_array.append([models.NameDetails(**doc) for doc in documento][0].__repr__())
        return JSONResponse(response_array)
            
        return response_array
    except Exception as e:
        return e
    
@router.get("/recommendations/")
async def generate_recommendations(request : Request):

    names_to_update = {}
    
    actions_db = request.app.database['actions']
    actions = actions_db.find({'relationalName' : {'$exists' : True}})

    names_list = set({}) #nomes a sofrerem alteracoes 
    for action in actions:
        names_list.add(action['name'])
        names_list.add(action['relationalName'])
        
    #Percorre a lista dos nomes
    for name in names_list:
        this_name_actions = list(actions_db.find({'$or' : [{'name' : name}, {'relationalName' : name}], 'userId' : {'$ne' : None}}))#todas as interações com o nome n

        usuarios = {} # usuario : peso
        this_name_actions.sort(key=lambda doc:doc['userId']) #ordena
        grouped_actionsby_users_for_this_name = groupby(this_name_actions, key=lambda doc : doc['userId'])

        for key, docs in grouped_actionsby_users_for_this_name: #Numero de interacoes do usuario u com o nome n
            usuarios[key] = 0
            for doc in docs:
                usuarios[key] +=1
            
        usuarios = sorted(usuarios.items(), key=lambda item : item[1], reverse=True)[0:30] #Ordena do maior para o menor e pega os 30 primeiros
        names = {}
        for user, peso in usuarios: #Obs: Considerar um único nome, ou mais de um nome?
            actions_of_user_u = actions_db.find({'userId' : user, 'relationalName' : {'$exists' : True}})
            for actions_of_u in actions_of_user_u:
                n_action = actions_of_u['name']
                nr_action = actions_of_u['relationalName']
                if n_action not in names:
                    names[n_action] = 0
                if nr_action not in names:
                    names[nr_action] = 0
                    names[n_action] += peso
                    names[nr_action] +=peso

        names_to_update[name] = names
    return {"names_to_update": names_to_update}
    # """
    # Gera recomendações temporárias para um usuário com base na interação de outros usuários.
    # """

    # actions_db = request.app.database['actions']

    # #  Buscar os nomes que o usuário interagiu
    # user_actions = list(actions_db.find({"userId": userId}, {"_id": 0, "name": 1}))
    # user_names = {action["name"] for action in user_actions}

    # if not user_names:
    #     return {"message": "Nenhuma interação encontrada para esse usuário."}

    # # 2️⃣ Buscar usuários que interagiram com os mesmos nomes
    # similar_users = set()
    # for name in user_names:
    #     other_users = actions_db.find({"name": name}, {"_id": 0, "userId": 1})
    #     similar_users.update(user["userId"] for user in other_users if user["userId"] != userId)

    # # 3️⃣ Coletar interações desses usuários e atribuir pesos
    # recommendations = defaultdict(int)
    # for similar_user in similar_users:
    #     actions = actions_db.find({"userId": similar_user, "relationalName": {"$exists": True}})
    #     for action in actions:
    #         n_action = action["name"]
    #         nr_action = action["relationalName"]

    #         if n_action not in user_names:  # Evita recomendar nomes que o usuário já interagiu
    #             recommendations[n_action] += 1
    #         if nr_action not in user_names:
    #             recommendations[nr_action] += 1

    # # 4️⃣ Ordenar recomendações pelo peso e retornar os 10 melhores
    # sorted_recommendations = sorted(recommendations.items(), key=lambda item: item[1], reverse=True)[:10]
    # recommended_names = [name for name, _ in sorted_recommendations]

    # return {"user_id": userId, "recommended_names": recommended_names}