
from fastapi import Depends, FastAPI, HTTPException,  status
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
session = database.get_db




@app.post("/data/", response_model=article_vm.ArticleCreateVM)
def create_data(data: article_vm.ArticleCreateVM, db: Session = Depends(session)):
    try:
        db_user = article_controller.create_data(db, data=data)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/data/search", response_model=list[article_vm.ArticleVM])
async def search_data(search_request: article_vm.ArticleSearch, db: Session = Depends(session)):
    try:
        query = search_request.query
        result = article_controller.search_data(db, query)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/data/filter", response_model=list[article_vm.ArticleVM])
async def filter_data(data: article_vm.ArticleFilterVM, db: Session = Depends(session)):
    try:
        result = article_controller.filter_data(db, data)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/data/get", response_model=list[article_vm.ArticleCreateVM])
def get_data(db: Session = Depends(session)):
    try:
        db_user = article_controller.get_data(db)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))