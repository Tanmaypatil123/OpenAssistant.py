from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel,Field ,Enum , JSON ,ForeignKey
from uuid import uuid4 ,UUID
from sqlalchemy import Column , DateTime , func
import enum
from typing import List

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

class RunStepType:
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


# class Assistant(SQLModel,table = True):
#     id : UUID = Field(default=uuid4(),primary_key=True)
#     created_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),server_default=func.now())
#     )
#     updated_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),onupdate=func.now())
#     )
#     description : Optional[str]
#     file_ids : List[str] = Field(default=[])
#     instructions : Optional[str]
#     metadata : JSON
#     model :str
#     name : Optional[str]
#     tools : List[JSON] = Field(default=[])
#     object : str = Field(default="assistant")
#     files : List["AssistantFile"] = Field(default=[])
#     message : List["Message"] = Field(default=[])
#     runs : List["Run"] = Field(default=[])
#     run_steps : List["RunStep"] = Field(default=[])


# class AssistantFile(SQLModel,table = True):
#     id : UUID = Field(default=uuid4(),primary_key=True,index=True)
#     created_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),server_default=func.now())
#     )
#     updated_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),onupdate=func.now())
#     )
#     assistant_d : int  = Field(foreign_key="assistant.id",index=True)
#     object : str

# class Message(SQLModel,table = True):
#     id : UUID = Field(default=uuid4(),primary_key=True,index=True)
#     created_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),server_default=func.now())
#     )
#     updated_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),onupdate=func.now())
#     )
#     content :List[JSON]
#     file_ids : List[str]
#     metadata : Optional[JSON]
#     role : Role
#     assistant_id = Field(foreign_key="assistant.id")
#     thread_id =  Field(foreign_key="thread.id")
#     run_id = Field(foreign_key="run.id")
#     object : str = Field(default="thread.message")
#     files : List["MessageFile"]


# class MessageFile(SQLModel,table = True):
#     id : UUID = Field(default=uuid4(),primary_key=True,index=True)
#     created_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),server_default=func.now())
#     )
#     updated_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),onupdate=func.now())
#     )

#     message_id = Field(foreign_key="message.id")
#     object : str = Field("thread.message.file")


# class Run(SQLModel,table = True):
#     id : UUID = Field(default=uuid4(),primary_key=True,index=True)
#     created_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),server_default=func.now())
#     )
#     updated_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),onupdate=func.now())
#     )
#     instructions : str
#     model : str
#     file_ids :  List[str]
#     metadata : Optional[JSON]
#     last_error : Optional[JSON]
#     tools : List[JSON]
#     status : RunStatus
#     started_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),server_default=func.now())
#     )
#     completed_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),server_default=func.now())
#     )
#     cancelled_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),server_default=func.now())
#     )
#     expires_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),server_default=func.now())
#     )
#     failed_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),server_default=func.now())
#     )
#     assistant_id = Field(foreign_key="assistant.id")
#     thread_id =  Field(foreign_key="thread.id")
#     object : str = Field(default="thread.run")
#     messages : List[Message]
#     run_steps : List["RunStep"]
    


# class RunStep(SQLModel,table = True):
#     id : UUID = Field(default=uuid4(),primary_key=True,index=True)
#     created_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),server_default=func.now())
#     )
#     updated_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),onupdate=func.now())
#     )
#     metadata : Optional[JSON]
#     last_error : Optional[JSON]
#     step_details : Optional[JSON]
#     status : RunStepStatus
#     type : RunStepType = Field(index=True)
#     completed_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),server_default=func.now())
#     )
#     cancelled_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),server_default=func.now())
#     )
#     expires_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),server_default=func.now())
#     )
#     failed_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),server_default=func.now())
#     )
#     assistant_id = Field(foreign_key="assistant.id")
#     thread_id =  Field(foreign_key="thread.id")
#     run_id = Field(foreign_key="run.id",index=True)
#     message_id : Optional[str]
#     object : str = Field(default="thread.run.step")



# class Thread(SQLModel,table = True):
#     id : UUID = Field(default=uuid4(),primary_key=True)
#     created_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),server_default=func.now())
#     )
#     updated_at : Optional[datetime] = Field(
#         sa_column=Column(DateTime(timezone=True),onupdate=func.now())
#     )
#     metadata : Optional[JSON]
#     object : str = Field(default="thread")
#     messages : List[Message]
#     run : List[Run]
#     run_steps : List[RunStep]