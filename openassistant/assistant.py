from openassistant.server import server
from fastapi import FastAPI
from typing import Optional
from langchain_core.language_models.llms import BaseLLM
from langchain_core.embeddings import Embeddings
import logging
import uvicorn
from chromadb import PersistentClient


logger = logging.getLogger(__name__)

class OpenAssistant:

    _server : FastAPI
    _llm : BaseLLM 
    _embeddings : Embeddings
    _name : str

    def __init__(self,llm : BaseLLM,embeddings : Embeddings , name : str):

        self._llm = llm
        self._embeddings = embeddings
        self._name = name
        self._server = server

    def serve(self):
        uvicorn.run(app=self._server)


