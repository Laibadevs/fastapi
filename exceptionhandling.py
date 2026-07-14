from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Custom exception
class UserNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name


# Exception handler
@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": f"User {exc.name} not found"
        }
    )


@app.get("/user/{name}")
def get_users(name: str):
    if name != "mohit":
        raise UserNotFoundException(name)   # Pass the name
    return {
        "name": name
    }


@app.get("/userid/{user_id}")
def get_user(user_id: int):
    if user_id != 1:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": 1,
        "name": "Mohit"
    }