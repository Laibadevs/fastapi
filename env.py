from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# import os
# from dotenv import load_dotenv
from config import settings

app = FastAPI()

# load_dotenv()

#Allowed Origins(Front-end URl)
origins = settings.origins
# SECRET_KEY= os.getenv("SECRET_KEY")
# DB_URL = os.getenv("DB_URL")

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins, #allowed FE
    allow_credentials = True,
    allow_methods = ["*"], #GET,PUT,POST,DELETE
    allow_headers=["*"]
)

@app.get("/")
def home():
    return{
        "message":"CORS ENABLE API"
    }