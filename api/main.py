
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from  models.base import Database
from controllers  import data_controller
import os,sys

import view_model.data_vm as data_vm

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




@app.post("/data/", response_model=data_vm.DataCreateVM)
def create_data(data:data_vm.DataCreateVM, db: Session = Depends(database.get_db)):
    db_user =  data_controller.create_data(db,  data = data)
    return db_user

    
@app.post("/data/search", response_model=list[data_vm.DataVM])
async def search_data(search_request: data_vm.DataSearch, db: Session = Depends(database.get_db)):
    query = search_request.query
    result = data_controller.search_data(db,query)
    return result

@app.get("/data/get", response_model=list[data_vm.DataCreateVM])
def get_data(db: Session = Depends(database.get_db) ):
    db_user =  data_controller.get_data(db)
    return db_user