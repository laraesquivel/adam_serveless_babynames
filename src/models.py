from pydantic import BaseModel, Field
#from pydantic.functional_validators import BeforeValidator
from typing import Optional, Annotated, List
from bson import ObjectId
from geojson import Point, Feature
import datetime
import pytz
import re



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
    _id: str = Field(..., alias="_id")
    similiarNames: List[str]
    name: str
    origin: str
    meaning: str

class NameDetails(BaseModel):
    _id: str = Field(..., alias="_id")
    similiarNames: List[str]
    name: str
    origin: str
    meaning: str
    associedDetails: Optional[List[SimilarNameDetails]] = None


class NameInfo(BaseModel):
    found: bool
    data: Optional[NameData]
    id : str


class NamesRequest(BaseModel):
    pass

class ActionRequest(BaseModel):
    item : str 
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
                "relationalNameID" : ObjectId(self.relationalNameID)}
        
        elif self.relationalNameID:
            return {'item' : self.item, 'action' : self.action,
                "tokenId" : self.tokenId,
               # "location" : location,
                "page" : self.page,
                "timestamp" : datetime.datetime.now(pytz.timezone("America/Bahia")).timestamp(),
                "action" : self.action,
               # "relationalItem" : self.relationalItem,
                "relationalNameID" : ObjectId(self.relationalNameID)}

    
        return {'item' : self.item, 'action' : self.action,
            "tokenId" : self.tokenId,
            "page" : self.page,
            "timestamp" : datetime.datetime.now(pytz.timezone("America/Bahia")).timestamp(),
            "action" : self.action}



class ActionResult(BaseModel):
    message: str
    id: str