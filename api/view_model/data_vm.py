from typing import Optional
from pydantic import BaseModel


class DataBaseVM(BaseModel):
    image_url : str 
    title : str
    article_url : str
    highlight : str
    time_publish : str
    category : str
    date_published : str
    publisher_name : str
    detail_content : str
   
   
class DataCreateVM(DataBaseVM):
    pass

class DataVM(DataBaseVM):
    id: int
   

    class Config:
        orm_mode = True



class DataSearch(BaseModel):
    query: str
    

class DataFilterVM(BaseModel):
    id:int | None = None
    image_url : str | None = None
    title : str | None = None
    article_url : str | None = None
    highlight : str | None = None
    time_publish : str | None = None
    category : str | None = None
    date_published : str | None = None
    publisher_name : str | None = None
    detail_content : str | None = None
   