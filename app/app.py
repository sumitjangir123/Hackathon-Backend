from fastapi import FastAPI
from fastapi.responses import JSONResponse,FileResponse
from applications.views import router as ApplicationRouter
from starlette.requests import Request
from config import Config
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware


 
origins = Config.origins


app = FastAPI()

@app.get("/static/img")
def read_root(fileName:str):
    return FileResponse("static/img/"+fileName,media_type="image/png")
    

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ApplicationRouter, tags=["applications"], prefix="/applications")
