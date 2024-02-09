from typing import Optional , Dict ,List
from datetime import datetime
from sqlmodel import SQLModel,Field ,Enum , JSON ,ForeignKey,Relationship
from uuid import uuid4 ,UUID
from sqlalchemy import Column , DateTime , func
import enum


class FileStatus(str , enum.Enum):
    ERROR = "error"
    PROCESSED = "processed"
    UPLOADED = "uploaded"

class Role(str,enum.Enum):
    ASSISTANT = "assistant"
    USER = "user"
    SYSTEM = "system"
    FUNCTION = "function"
    TOOL = "tool"

class RunStatus(str,enum.Enum):
    CANCELLED = "cancelled"
    CANCELLING = "cancelling"
    COMPLETED = "completed"
    EXPIRED = "expired"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    QUEUED = "queued"
    REQUIRED_ACTION = "required_action"

class RunStepStatus(str,enum.Enum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    EXPIRED = "expired"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"

class RunStepType(str,enum.Enum):
    MESSAGE_CREATION = "message_creation"
    TOOL_CALLS = "tool_calls"

class ToolCallType(str,enum.Enum):
    FUNCTION = "function"
    CODE_INTERPRETER = "code_interpreter"
    RETRIEVAL = "retrieval"

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
    status : FileStatus
    status_details : Optional[str] = Field(default="file")


class Assistant(SQLModel,table = True):
    id : UUID = Field(default=uuid4(),primary_key=True)
    created_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),server_default=func.now())
    )
    updated_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),onupdate=func.now())
    )
    description : Optional[str]
    file_ids : List[str] = Field(sa_column=Column(JSON))
    instructions : Optional[str]
    meta_data : Dict = Field(sa_column=Column(JSON),default={})
    model :str
    name : Optional[str]
    tools : Dict = Field(sa_column=Column(JSON),default={})
    object : str = Field(default="assistant")
    files: List["AssistantFile"] = Relationship(back_populates="assistant")
    
    message : List["Message"] =  Relationship(back_populates="message")
    runs : List["Run"] = Relationship(back_populates="run")
    run_steps : List["RunStep"] = Relationship(back_populates="runstep")


class AssistantFile(SQLModel,table = True):
    id : UUID = Field(default=uuid4(),primary_key=True,index=True)
    created_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),server_default=func.now())
    )
    updated_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),onupdate=func.now())
    )
    assistant_id : UUID  = Field(foreign_key="assistant.id",index=True)
    object : str

class Message(SQLModel,table = True):
    id : UUID = Field(default=uuid4(),primary_key=True,index=True)
    created_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),server_default=func.now())
    )
    updated_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),onupdate=func.now())
    )
    content :List[str] = Field(sa_column=Column(JSON))
    file_ids : List[str] = Field(sa_column=Column(JSON))
    meta_data : Dict = Field(sa_column=Column(JSON),default={})
    role : Role
    assistant_id : UUID= Field(foreign_key="assistant.id")
    thread_id : UUID =  Field(foreign_key="thread.id")
    run_id : UUID = Field(foreign_key="run.id")
    files : List["MessageFile"] = Relationship(back_populates="messagefile")
    object : str = Field(default="thread.message")
    


class MessageFile(SQLModel,table = True):
    id : UUID = Field(default=uuid4(),primary_key=True,index=True)
    created_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),server_default=func.now())
    )
    updated_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),onupdate=func.now())
    )

    message_id: UUID = Field(foreign_key="message.id")
    object : str = Field("thread.message.file")


class Run(SQLModel,table = True):
    id : UUID = Field(default=uuid4(),primary_key=True,index=True)
    created_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),server_default=func.now())
    )
    updated_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),onupdate=func.now())
    )
    instructions : str
    model : str
    file_ids :  List[str] = Field(sa_column=Column(JSON))
    meta_data : Dict = Field(sa_column=Column(JSON),default={})
    last_error : Optional[Dict] = Field(sa_column=Column(JSON),default={})
    tools : List[str] =  Field(sa_column=Column(JSON),default={}) 
    status : RunStatus
    started_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),server_default=func.now())
    )
    completed_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),server_default=func.now())
    )
    cancelled_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),server_default=func.now())
    )
    expires_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),server_default=func.now())
    )
    failed_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),server_default=func.now())
    )
    assistant_id : UUID = Field(foreign_key="assistant.id")
    thread_id  : UUID=  Field(foreign_key="thread.id")
    object : str = Field(default="thread.run")
    messages : List[Message] = Relationship(back_populates="message")
    run_steps : List["RunStep"] = Relationship(back_populates="runstep")
    


class RunStep(SQLModel,table = True):
    id : UUID = Field(default=uuid4(),primary_key=True,index=True)
    created_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),server_default=func.now())
    )
    updated_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),onupdate=func.now())
    )
    meta_data : Dict = Field(sa_column=Column(JSON),default={})
    last_error : Optional[Dict] = Field(sa_column=Column(JSON),default={})
    step_details :Optional[Dict] = Field(sa_column=Column(JSON),default={})
    status : RunStepStatus
    type : RunStepType = Field(index=True)
    completed_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),server_default=func.now())
    )
    cancelled_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),server_default=func.now())
    )
    expires_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),server_default=func.now())
    )
    failed_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),server_default=func.now())
    )
    assistant_id : UUID = Field(foreign_key="assistant.id")
    thread_id : UUID =  Field(foreign_key="thread.id")
    run_id : UUID = Field(foreign_key="run.id",index=True)
    message_id : Optional[str]
    object : str = Field(default="thread.run.step")



class Thread(SQLModel,table = True):
    id : UUID = Field(default=uuid4(),primary_key=True)
    created_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),server_default=func.now())
    )
    updated_at : Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),onupdate=func.now())
    )
    meta_data : Dict = Field(sa_column=Column(JSON),default={})

    object : str = Field(default="thread")
    messages : List[Message] = Relationship(back_populates="message")
    run : List[Run] = Relationship(back_populates="run")
    run_steps : List[RunStep] = Relationship(back_populates="runstep")