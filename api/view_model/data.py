from typing import Optional
from pydantic import BaseModel


class DataBase(BaseModel):
    image_url : str 
    title : str
    article_url : str
    highlight : str
    time_publish : str
    category : str
    date_published : str
    publisher_name : str
    detail_content : str
   
   
class DataCreate(DataBase):
    pass

class Data(DataBase):
    id: int
   

    class Config:
        orm_mode = True
