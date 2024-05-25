from sqlalchemy import  Column,  Integer, String
from .database import Base

class TelegramArticle(Base):
    __tablename__ = "telegram_articles"

    id = Column(Integer, primary_key=True)
    channel = Column(String)
    message = Column(String)
    date =  Column(String)
    

    
    