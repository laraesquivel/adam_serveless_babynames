from pydantic import BaseModel, Field
#from pydantic.functional_validators import BeforeValidator
from typing import Optional, Annotated, List
from bson.objectid import ObjectId as MONGO_ID
from bson import Timestamp
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
    recommendedNames : Optional[str]

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
    name : str 
    nameID : Optional[str]
    userId :Optional[str] 
    action : int 
    lat : Optional[float]
    lon : Optional[float]
    page : int 
    location : Optional[Point] = None
    timestamp : Optional[float]
    relationalName : Optional[str]
    relationalNameID : Optional[str]
   # idName : str
    
       


class ActionResult(BaseModel):
    message: str
    id: str


class User(BaseModel):
    userId : str

class UserResponse(BaseModel):
    userId : str
    id : Optional[PydanticObjectId] = Field(alias= '_id')

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            MONGO_ID: lambda x: str(x)
        }

    def __repr__(self) -> str:
        return {
            'userId' : self.userId,
            'id' : self.id
        }
