# from typing import Annotated
# from pydantic import BaseModel, Field
# from sqlalchemy.orm import Session
from starlette import status

from models import Todos

# from fastapi import FastAPI, Depends, HTTPException, Path
from fastapi import FastAPI, HTTPException, Path
import models
from database import engine
# from database import engine,SessionLocal
from routers import auth,todos,admin,users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
#auth.py file is a route instead of entire app so we include autn.py file as the route of this app
# After this you get auth route on top of your todos route in swagger UI
app.include_router(todos.router)#New
app.include_router(admin.router)# after this we get a new section admin with the functionalities that is in admin.py
app.include_router(users.router)

# we just cleaned our application for maintainbility and scalability by making routers package me auth.py and todos.py

# Rest we can delete as router me kaam hogaya hai and also unneeded imports delete
#
#
# def get_db():
#     db=SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# db_dependency=Annotated[Session,Depends(get_db)]
#
# class TodoRequest(BaseModel):#only Id not there because this is the primary key and we autoincrement it
#     title: str = Field(min_length=3)
#     description: str = Field(min_length=3,max_length=100)
#     priority: int = Field(gt=0,lt=6)
#     complete: bool# only 2 options so no validation
#
# @app.get("/",status_code=status.HTTP_200_OK)
# async def read_all(db:db_dependency):
#     return db.query(Todos).all()
#
# @app.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
# async def read_all(db:db_dependency,todo_id: int = Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id==todo_id).first()
#     if todo_model is not None:
#         return todo_model
#     raise HTTPException(status_code=404,detail='Todo not found')
#
# @app.post("/todo",status_code=status.HTTP_201_CREATED)
# async def create_todo(db: db_dependency, todo_request: TodoRequest):
#     todo_model=Todos(**todo_request.dict())
#
#     db.add(todo_model)
#     db.commit()
#
# @app.post("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
# async def update_todo(db:db_dependency, todo_request:TodoRequest,todo_id: int= Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id==todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404,detail='Todo not found')
#
#     todo_model.title=todo_request.title
#     todo_model.description = todo_request.description
#     todo_model.priority = todo_request.priority
#     todo_model.complete = todo_request.complete
#
#     db.add(todo_model)
#     db.commit()

#
# @app.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
# async def delete_todo(db:db_dependency,todo_id: int= Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id==todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404,detail='Todo not found')
#
#     db.query(Todos).filter(Todos.id==todo_id).delete()
#
#     db.commit()
#
#
#
#

# app.include_router(auth.router)
# app.include_router(todos.router)
# app.include_router(admin.router)
# app.include_router(users.router)