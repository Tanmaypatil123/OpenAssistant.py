from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel,Field ,Enum
from uuid import uuid4 ,UUID
from sqlalchemy import Column , DateTime , func
import enum


class FileStatus(enum.Enum):
    ERROR = "error"
    PROCESSED = "processed"
    UPLOADED = "uploaded"

class Files(SQLModel,table = True):
    id : UUID = Field(default=uuid4(),primary_key=True)
    created_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),server_default=func.now())
    )
    updated_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),onupdate=func.now())
    )

    _bytes : int = None
    filename : str
    purpose : str = Field(index=True)
    status : Optional[Enum[FileStatus]] = Field(sa_column=Column(Enum(FileStatus)))
    status_details : Optional[str] = Field(default="file")

class Assistant(SQLModel,table = True):
    pass


class AssistantFile(SQLModel,table = True):
    pass


class Thread(SQLModel,table = True):
    pass

class Message(SQLModel,table = True):
    pass

class MessageFile(SQLModel,table = True):
    pass

class Run(SQLModel,table = True):
    pass

class RunStep(SQLModel,table = True):
    pass
