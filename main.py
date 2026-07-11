from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()
class User(BaseModel):
    name:str
    age:int
@app.get("/")
def home():
     return {"message":"Hello without vern"}


@app.get("/about")
def about():
    return {"message":"this is about page"}
 #path parameter
# @app.get("/users/{users_id}")
# def get_user(users_id:int):
#   return {"user_id":users_id}

#query parameters
# @app.get("/users")
#query
# def get_users(name ):
#     return {"Name":name}
#optional
def get_users(name: str=None):
    return {"Name":name}
#default value
@app.get("/products")
def get_users(limit: int=10):
    return{"limit":limit}
#multiple paramerts
@app.get("/items")
def get_users( name:str=None, price: int=10):
    return{"name":name,
            "price":price
    }

# post requests
@app.post("/create-user")
# def create_user(name:str,age:int):
#     return{
#         "name":name,
#         "age":age
#     }
def create_user(user:User):
    return{
    "message":"User created",
    "data":user
    }