from typing import Optional
from pydantic import BaseModel


class TelegramArticleBaseVM(BaseModel):
    channel : str
    message : str
    date : str
   
   
class TelegramArticleCreateVM(TelegramArticleBaseVM):
    pass

class TelegramArticleVM(TelegramArticleBaseVM):
    id: int
   

    class Config:
        orm_mode = True



class TelegramArticleSearch(BaseModel):
    query: str
    

class TelegramArticleFilterVM(BaseModel):
    id:int | None = None
    channel : str | None = None
    message : str | None = None
    date : str | None = None
   
   