from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()

#path + query

user=[]
class User (BaseModel):
    name:str
    age:int
@app.post("/users")
def create_user(user:User):
    users.append(user)
    return{
        "message":"User created",
    }
@app.put("/users/{user_id}")
def updated_user(user_id:int,user:User,notify:bool=False):
    if user_id < len(users):
        user[user_id]=user
        return{
            "message":"User Updated",
            "notify":notify,
            "data":user
        }
    return{
        "error":"User not found"
    }