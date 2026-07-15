from fastapi import FastAPI, HTTPException, Depends, Header
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
app=FastAPI()

#secure
SECRET_KEY="mysecret"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
#PASSWORD HASHING SETUP
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#outhsetup
oauth2_schema=OAuth2PasswordBearer(tokenUrl="login")
#Dummy user Db
fake_user_db={
    "admin":{
        "username":"admin",
        "hashed_password":pwd_context.hash("1234")
    }
}
#hash password
def hash_password(password:str):
    return pwd_context.hash(password)
#varify passowrd
def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
#token function,create token
def create_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=30)
    # add expire into payload
    to_encode.update({
        "exp":expire  
    })
    #token generate
    token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token
#generate token base on logging api (oauth)
# @app.post("/login")
# def login(username:str,password:str):
#     if username!="admin" or password !="1234":
#      raise HTTPException(
#         status_code=401,
#         detail="Invalid username and password"
#      )
#     token = create_token ({
#         "sub":username
#     })
#     return {
#         "access_token":token
#     }

@app.post("/login")
def login(form_data:OAuth2PasswordRequestForm=Depends()):
    user=fake_user_db.get(form_data.username)
    if not user or not verify_password(form_data.password,user["hashed_password"]):
        raise HTTPException(
            status_code=400,
            detail="Invalid username or password"
        )
    access_token=create_token({"sub":form_data.username})
    return{
        "access_token":access_token,
        "token_type":"bearer"
    }
#verify token
# def verify_token(token:str=Header(None)):
#     try:
#         payload= jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
#         return payload
#     except:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid or expired to"
#         )
def verify_token(token: str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return username

    except jwt.JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
@app.get("/secure")
def secure_data(username:str =Depends(verify_token)):
    return{
        "message":f"hello {username}, you have access to this protected route",
        "user":username
    }