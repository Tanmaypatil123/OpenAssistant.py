from .schemas import *
from sqlmodel import create_engine

class DatabaseClient:
    """
    Database client for connection with relational database.
    """
    def __init__(self,path_db : str) -> None:
        self.dialect = "sqlite"
        self.path_to_db = path_db
        

    def connect(self):
        self.engine = create_engine(f"{self.dialect}:///{self.path_to_db}",echo=True)
        SQLModel.metadata.create_all(self.engine)
        