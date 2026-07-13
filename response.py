from fastapi import FastAPI
from pydantic import  BaseModel
app=FastAPI()
# {
#     "name":"Mohit",
#     "age":25,
#     "password":1234 
# }
class User(BaseModel):
    name:str
    age:int
    password:str
class UserResponse(BaseModel):
    name:str
    age:int
@app.get("/user", response_model=UserResponse)
def get_user():
    return{
        "name":"Mohit",
        "age":24,
        "password":"12345"
    }