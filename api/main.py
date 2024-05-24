
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from  models.database import Database
from controllers  import article_controller
import os

import view_model.article_vm as article_vm

from dotenv import load_dotenv

load_dotenv()
rpath = os.path.abspath('../api')
SQLALCHEMY_DATABASE_URL = os.getenv('DB_CONNECTION_STRING')

app = FastAPI(
        title="Amharic data integration for LLM",
        description="",
        version="1"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



database = Database(SQLALCHEMY_DATABASE_URL)




@app.post("/data/", response_model=article_vm.ArticleCreateVM)
def create_data(data:article_vm.ArticleCreateVM, db: Session = Depends(database.get_db)):
    db_user =  article_controller.create_data(db,  data = data)
    return db_user

    
@app.post("/data/search", response_model=list[article_vm.ArticleVM])
async def search_data(search_request: article_vm.ArticleSearch, db: Session = Depends(database.get_db)):
    query = search_request.query
    result = article_controller.search_data(db,query)
    return result

@app.post("/data/filter", response_model=list[article_vm.ArticleVM])
async def search_data(data: article_vm.ArticleFilterVM, db: Session = Depends(database.get_db)):
    result = article_controller.filter_data(db,data)
    return result

@app.get("/data/get", response_model=list[article_vm.ArticleCreateVM])
def get_data(db: Session = Depends(database.get_db) ):
    db_user =  article_controller.get_data(db)
    return db_user