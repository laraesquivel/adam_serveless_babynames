def pipeline(n):

    pipeline = [
    {"$match": {"name": n}},
    {"$lookup": {
        "from": "names",
        "localField": "recommendedNames",
        "foreignField": "name",
        "as": "associedDetails"
    }},
    
    {"$project": {
        "_id": 1,
        "name": 1,
        "origin": 1,
        "meaning": 1,
        "similiarNames": 1,
        "associedDetails": 1
    }},
    {"$addFields": {
        "_id": {"$toString": "$_id"},
        "associedDetails": {
            "$map": {
                "input": "$associedDetails",
                "as": "detail",
                "in": {
                    "_id": {"$toString": "$$detail._id"},
                    "name": "$$detail.name",
                    "origin": "$$detail.origin",
                    "meaning": "$$detail.meaning",
                    "similiarNames": "$$detail.similiarNames"
                }
            }
        }
    }}
]
    return pipeline

def phrases_pipeline(n):
    pipeline = [
        {"$in": {"name": n}},
        {"$lookup": {
            "from": "names",
            "localField": "recommendedNames",
            "foreignField": "name",
            "as": "associedDetails"
        }},
        
        {"$project": {
            "_id": 1,
            "name": 1,
            "origin": 1,
            "meaning": 1,
            "similiarNames": 1,
            "associedDetails": 1
        }},
        {"$addFields": {
            "_id": {"$toString": "$_id"},
            "associedDetails": {
                "$map": {
                    "input": "$associedDetails",
                    "as": "detail",
                    "in": {
                        "_id": {"$toString": "$$detail._id"},
                        "name": "$$detail.name",
                        "origin": "$$detail.origin",
                        "meaning": "$$detail.meaning",
                        "similiarNames": "$$detail.similiarNames"
                    }
                }
            }
        }}
    ]
    return pipeline