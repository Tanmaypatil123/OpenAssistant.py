from fastapi import FastAPI
from .routes.router import router

server = FastAPI()

server.include_router(router=router)