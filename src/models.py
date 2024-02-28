from pydantic import BaseModel
from typing import Optional



class NameData(BaseModel):
    oid: str = ''
    closersNames: list[str] =''
    gender: str =''
    frequencyFemale: int = 0
    frequencyTotal: int = 0
    frequencyGroup: int =0
    searched: int =0
    name: str = ''
    groupName: str = ''
    recommendedNames: list[str] = ''

class NameInfo(BaseModel):
    found: bool
    data: Optional[NameData]