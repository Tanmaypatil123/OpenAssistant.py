from fastapi import APIRouter


router = APIRouter()

@router.get("/ping")
def ping():
    return {
        "message" : "server i running :) ."
    }


###############  FILE ROUTES ###############

@router.get("/api/files")
def get_files():
    pass



###############  Assistant  ROUTES ###############

@router.get("/api/assistant")
def get_assistants():
    pass

###############  Thread  ROUTES ###############

@router.get("/api/threads")
def get_threads():
    pass