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

ALL_ORIGIN = ["Alemã", "Árabe", "Espanhola", "Francesa", "Grega", "Hebraica", "Indígena", "Inglesa", "Japonesa", "Lusitana"]
ALL_BRAZIL_REGION = ['Região Norte', 'Região Nordeste', 'Região Centro-Oeste', 'Região Sudeste', 'Região Sul']
GENDER = ['M', 'F']

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
        #print("Resultados brutos do pipeline:", results)
        
        if not results:
            raise HTTPException(status_code=404, detail="Nome não encontrado na lista de nomes.")
        
        # Remove duplicatas
        unique_results = {item['name']: item for item in results}  # Dicionário para remover nomes duplicados
        filtered_results = list(unique_results.values())[:10]  # Garante no máximo 10 nomes

        print(f"Resultados filtrados: {filtered_results}")
        
        #print(f"Resultados do banco: {results}")

        name_details = [models.NameDetails(**item) for item in filtered_results]
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

# @router.get('/getActualPhrase')
# def get_actual_phrase(request : Request, userId : str = None):
#     # Seleciona uma frase aleatória do banco de dados e envia para o usuário
#     try:
#         if not userId:
#             raise HTTPException(status_code=400, detail="Por favor, forneça um userId para pesquisar na lista de nomes.")
        
#         users_collection = request.app.database['users'] 
#         babynames = request.app.database["newNames"]
#         babynames_phrases = request.app.database["phrases"]
        
#         # Verifica se o usuário já existe no banco de dados
#         user = users_collection.find_one({"userId": userId})
        
#         if not user:
#             raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        
#         # Verifica se o usuário já possui uma frase associada
#         if "phrase" in user and user["phrase"]:
#             return JSONResponse(user["phrase"])
        
#         # Seleciona uma frase aleatória do banco de dados
#         random_phrase = babynames_phrases.aggregate([{"$sample": {"size": 1}}])
#         phrase = list(random_phrase)[0]["phrase"]
        
#         # Atualiza o usuário com a nova frase
#         users_collection.update_one({"userId": userId}, {"$set": {"phrase": phrase}})
        
#         return JSONResponse(phrase)
#     except Exception as e:
#         return JSONResponse(json_util.dumps({'message':e}),status_code=500)

#-----------------------------------------------------------------------------------------------------------------------
# Funções para recomendação de frases em tempo real
# Função auxiliar
# def binarize_preferences(G, R, O):
#     def __binarization(lst):
#         max_idx = 0
#         swap = False
#         new_list = [0] * len(lst)
#         for idx in range(len(lst)):
#             if lst[idx - 1] > lst[max_idx]:
#                 max_idx = idx - 1
#                 swap = True
#         if swap:
#             new_list[max_idx] = 1
#         return new_list

#     origin_list = __binarization([O.get(o, 0) for o in ALL_ORIGIN])
#     gender_list = __binarization([G.get(g, 0) for g in GENDER])
#     region_list = __binarization([R.get(r, 0) for r in ALL_BRAZIL_REGION])
#     binary_str = ''.join(map(str, gender_list + region_list + origin_list))
#     return binary_str

# # ⬇️ GET para atualizar a assinatura (assignature) do usuário
# @router.get("/update_user_assignature")
# def update_user_assignature(request: Request, userId: str):
#     db = request.app.database
#     users = db['users']
#     actions = db['actions']
#     names = db['newNames']
#     location = db['location']

#     user = users.find_one({'userId': userId})
#     if not user:
#         raise HTTPException(status_code=404, detail="Usuário não encontrado")

#     G, R, O = {}, {}, {}

#     this_user_actions = actions.find({'userId': userId})
#     for action in this_user_actions:
#         name_data = names.find_one({'name': action['name'], 'origin': {'$exists': True}})
#         if name_data:
#             g = name_data.get('gender')
#             o = name_data.get('origin')
#             if g:
#                 G[g] = G.get(g, 0) + 1
#             if o:
#                 O[o] = O.get(o, 0) + 1

#         loc = location.find_one({'_id': action['location']})
#         if loc:
#             region = loc.get('region')
#             if region:
#                 R[region] = R.get(region, 0) + 1

#     assignature = binarize_preferences(G, R, O)
#     users.update_one({'userId': userId}, {
#         '$set': {
#             'preferences': {'gender': G, 'region': R, 'origin': O},
#             'assignature': assignature
#         }
#     })
#     return {'status': 'ok', 'assignature': assignature}


# # ⬇️ GET para atualizar a recomendação de frases do usuário
# @router.get("/update_user_phrases")
# def update_user_phrases(request: Request, userId: str):
#     db = request.app.database
#     users = db['users']
#     phrases = db['phrases']

#     user = users.find_one({'userId': userId})
#     if not user:
#         raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
#     if 'assignature' not in user:
#         raise HTTPException(status_code=400, detail="Usuário não possui assinatura (assignature)")
    
#     if 'phrases' in user:
#         return {'status': 'phrases já atribuídas'}

#     assignature = user['assignature']
#     matching_phrases = list(phrases.find({'assignature': assignature}))
    
#     users.update_one({'userId': userId}, {'$set': {'phrases': matching_phrases}})
#     return {'status': 'phrases atualizadas', 'total': len(matching_phrases)}
    
#-----------------------------------------------------------------------------------------------------------------------
# FUNÇÃO TESTE PARA GERAR RECOMENDAÇÕES INDIVIDUAIS (NÃO SERÁ USADA NO MOMENTO)
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
    return {"message" : "Recomendações geradas com sucesso"}