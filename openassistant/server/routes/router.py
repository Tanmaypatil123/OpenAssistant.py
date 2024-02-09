from fastapi import APIRouter ,File,Form,UploadFile
from openassistant.dbs.client import DatabaseClient
from sqlmodel import Session , select 
from openassistant.dbs.schemas import Files ,FileStatus
import json
from typing import Annotated
from fastapi.responses import FileResponse

router = APIRouter()
sql_engine = DatabaseClient(path_db="db.sqlite")
sql_engine.connect()

@router.get("/ping")
def ping():
    return {
        "message" : "server i running :) ."
    }


###############  FILE ROUTES ###############

### get all the file for purpose
@router.get("/api/files")
def get_files_by_id(purpose:str):
    with Session(sql_engine.engine) as session :
        statement = select(Files).where(Files.purpose == purpose)
        res = session.exec(statement).all()
        print(res)
    
    return {
        "data" : json.dumps([i.model_dump_json() for i in res])
    }

@router.post("/api/files")
def create_files(files : Annotated[UploadFile,File()],purpose : Annotated[str,Form()]):
    file_name = files.filename
    file_location = f"uploads/{file_name}"
    with open(file_location,"wb+") as file_object :
        file_object.write(files.file.read())
    
    with Session(sql_engine.engine) as session:
        print('Inserting data in database')
        model = Files(
            purpose=purpose,
            filename=file_name,
            status=FileStatus.UPLOADED
        )
        session.add(model)

        session.commit()
        data = model.id
    return {
        "file_id" : data
    }

@router.delete("/api/files/{file_id}")
def delete_file(file_id : str):
    with Session(sql_engine.engine) as session :
        statement = select(Files).where(Files.id == file_id)
        results = session.exec(statement=statement)
        file = results.one()
        session.delete(file)
        session.commit()

    return {
        "file_id" : file_id,
        "msg" : "Succesfully Deleted"
    }

@router.get("/api/files/{file_id}")
def retrieve_file(file_id : str):
    with Session(sql_engine.engine) as session :
        statement = select(Files).where(Files.id == file_id)
        results = session.exec(statement=statement)
        file = results.one()
        file_path = f"uploads/{file.filename}"

    return FileResponse(file_path)

@router.get("/api/files/{file_id}/content")
def get_content(file_id : str):
    with Session(sql_engine.engine) as session :
        statement = select(Files).where(Files.id == file_id)
        results = session.exec(statement=statement)
        file = results.one()
        file_path = f"uploads/{file.filename}"
    
    with open(file_path,"r") as file_object :
        data = file_object.read()

    return {
        "content" : data
    }
###############  Assistant  ROUTES ###############

@router.get("/api/assistant")
def get_assistants():
    pass

###############  Thread  ROUTES ###############

@router.get("/api/threads")
def get_threads():
    pass