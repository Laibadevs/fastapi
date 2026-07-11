from fastapi import FastAPI
app=FastAPI()

#home Route
@app.get("/")
def home ():
    return {"message":"welcome to fastapi"}
#about route
@app.get("/about")
def about():
    return {"message":"this is about page"}

#user route
@app.get("/users")
def users():
    return
    {
        "user":["Mohit","Rohit","Amit"]
    }