from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import FastAPI, Depends

app = FastAPI()

DATABASE_URL = "sqlite:///./alch.db"

# Database connection
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session
SessionLocal = sessionmaker(bind=engine)

# Base class
Base = declarative_base()


# Model
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(String)


# Create tables
Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get("/")
# def home(db: Session = Depends(get_db)):
#     return {
#         "message": "DB connected successfully"
#     }
@app.post("/todos")
def create_todo(title:str, db:Session= Depends(get_db)):
 todo=Todo(title=title,completed="False")
 db.add(todo)
 db.commit()
 db.refresh(todo)
 return{
    "message":"todo created",
     "data":todo
 }

#read all data
@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return {
        "total": len(todos),
        "data": todos
    }

#read data based on id
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo

#update data
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, title: str, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.title = title
    db.commit()
    db.refresh(todo)

    return {
        "message": "Todo Updated",
        "data": todo
    }
#delete
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return{
        "message": "Todo Deleted",
       
    }