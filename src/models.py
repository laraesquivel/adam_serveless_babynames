from pydantic import BaseModel, Field
#from pydantic.functional_validators import BeforeValidator
from typing import Optional, Annotated, List
from bson.objectid import ObjectId as MONGO_ID
from geojson import Point, Feature
import datetime
import pytz
import re

class PydanticObjectId(MONGO_ID):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls,v):
        if not MONGO_ID.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return MONGO_ID(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class NameQuery(BaseModel):
    name : str

    def __repr__(self) -> str:
        remove_accent_and_capitalize = lambda s: re.sub(r'\p{M}', '', s.title())
        return remove_accent_and_capitalize(self.name)


class NameData(BaseModel):

    similiarNames: list[str] =''
    gender: str =''
    femaleCount : Optional[int] = 0
    maleCount : Optional[int] = 0
    count: int = 0
    groupCount: int =0
    searchedCount: int =0
    name: str = ''
    groupName: str = ''
    recommendedNames: list[str] = ''
    origin : str = ''
    meaning : str = ''

class SimilarNameDetails(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias='_id')
    similiarNames: Optional[List[str]]
    name: str
    origin: Optional[str]
    meaning: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            MONGO_ID: lambda x: str(x)
        }

    def __repr__(self) -> str:
        response_dict = {
            "id" : str(self.id),
            "similiarNames" : self.similiarNames,
            "name" : self. name,
            "origin" : self.origin,
            "meaning" : self.meaning,
        }

        return response_dict
    
class NameDetails(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias='_id')
    similiarNames: List[str]
    name: str
    origin: Optional[str]
    meaning: Optional[str]
    associedDetails: Optional[List[SimilarNameDetails]] = None
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            MONGO_ID: lambda x: str(x)
        }

    def __repr__(self) -> str:
        response_dict = {
            "id" : str(self.id),
            "similiarNames" : self.similiarNames,
            "name" : self. name,
            "origin" : self.origin,
            "meaning" : self.meaning,
            "associedDetails" : [item.__repr__() for item in self.associedDetails]
        }

        return response_dict

class NameInfo(BaseModel):
    found: bool
    data: Optional[NameData]
    id : str


class NamesRequest(BaseModel):
    pass

class ActionRequest(BaseModel):
    item : str 
    itemID : Optional[str]
    tokenId :Optional[str] 
    action : int 
    lat : Optional[float]
    lon : Optional[float]
    page : int 
    location : Optional[Point]
    timestamp : Optional[float]
    relationalItem : Optional[str]
    relationalNameID : Optional[str]
   # idName : str

    def __repr__(self) -> str:
        location = None
        if self.lat and self.lon and self.relationalNameID:
            location = Point((self.lat,self.lon))
    
            return {'item' : self.item, 'action' : self.action,
                "tokenId" : self.tokenId,
                "location" : location,
                "page" : self.page,
                "timestamp" : datetime.datetime.now(pytz.timezone("America/Bahia")).timestamp(),
                "action" : self.action,
                #"relationalItem" : self.relationalItem,
                "relationalNameID" : MONGO_ID(self.relationalNameID)}
        
        elif self.relationalNameID:
            return {'item' : self.item, 'action' : self.action,
                "tokenId" : self.tokenId,
               # "location" : location,
                "page" : self.page,
                "timestamp" : datetime.datetime.now(pytz.timezone("America/Bahia")).timestamp(),
                "action" : self.action,
               # "relationalItem" : self.relationalItem,
                "relationalNameID" : MONGO_ID(self.relationalNameID)}

    
        return {'item' : self.item, 'action' : self.action,
            "tokenId" : self.tokenId,
            "page" : self.page,
            "timestamp" : datetime.datetime.now(pytz.timezone("America/Bahia")).timestamp(),
            "action" : self.action}



class ActionResult(BaseModel):
    message: str
    id: str