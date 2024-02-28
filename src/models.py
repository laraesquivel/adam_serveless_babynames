from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from geojson import Point, Feature
import datetime
import pytz



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


class NameInfo(BaseModel):
    found: bool
    data: Optional[NameData]

class ActionRequest(BaseModel):
    item : str 
    tokenId :Optional[str] 
    action : int 
    lat : Optional[float]
    lon : Optional[float]
    page : int 
    location : Optional[Point]
    timestamp : Optional[float]

    def __repr__(self) -> str:
        location = None
        if self.lat and self.lon:
            location = Point((self.lat,self.lon))
    
            return {'item' : self.item, 'action' : self.action,
                "tokenId" : self.tokenId,
                "location" : location,
                "page" : self.page,
                "timestamp" : datetime.datetime.now(pytz.timezone("America/Bahia")).timestamp(),
                "action" : self.action}

    
        return {'item' : self.item, 'action' : self.action,
            "tokenId" : self.tokenId,
            "page" : self.page,
            "timestamp" : datetime.datetime.now(pytz.timezone("America/Bahia")).timestamp(),
            "action" : self.action}



class ActionResult(BaseModel):
    message: str
    id: str