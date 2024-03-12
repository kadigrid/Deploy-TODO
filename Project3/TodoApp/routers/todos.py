#we copied everything from main.py file to todos.py file and chnaged somethings written in comments + api endpoints me change app to router and in main.py file import todos.py from router
#May get Issues because we aren't inside a python project but a directory which has a python project inside
# So we open Todoapp directly in pycharm
# make sure you change todos folder interpreter to 3.11 python , It shows like Python 3.11(fastapienv)



from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from models import Todos

# from fastapi import FastAPI, Depends, HTTPException, Path# we changed here while copying
from fastapi import APIRouter, Depends, HTTPException, Path
# import models# we don't need it
# from database import engine,SessionLocal# we changed here while copying
from database import SessionLocal
# from routers import auth# we don't need it

from .auth import get_current_user#helps us to validate JWT and turn into username and userID

router = APIRouter()
# app = FastAPI()# we changed here while copying

# models.Base.metadata.create_all(bind=engine)
# WE removed these 2 lines
# app.include_router(auth.router)



def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]



class TodoRequest(BaseModel):#only Id not there because this is the primary key and we autoincrement it
    title: str = Field(min_length=3)
    description: str = Field(min_length=3,max_length=100)
    priority: int = Field(gt=0,lt=6)
    complete: bool# only 2 options so no validation

# @router.get("/",status_code=status.HTTP_200_OK)
# async def read_all(db:db_dependency):
#     return db.query(Todos).all()

# @router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)# Isme signin nahi karna padta
# async def read_all(db:db_dependency,todo_id: int = Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id==todo_id).first()
#     if todo_model is not None:
#         return todo_model
#     raise HTTPException(status_code=404,detail='Todo not found')

# isme signin karke diff. users ke hisaab se todos nikal sakte ho# also if you login in one api endpoint then the session is valid in other api endpoints as well in Swagger UI
#Path shouldn't be : /todo/{todo_id}
@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found.')

@router.post("/todo",status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model=Todos(**todo_request.dict(), owner_id=user.get('id'))# seperately owner id because yahan coversion me owner id nahi hai so seperately added

    db.add(todo_model)
    db.commit()

@router.post("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency,db:db_dependency, todo_request:TodoRequest,todo_id: int= Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id) \
        .filter(Todos.owner_id == user.get('id')).first()
    # todo_model = db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail='Todo not found')
#only put these field in Swagger UIin description
    todo_model.title=todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()



# @router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)# No Authentication
# async def delete_todo(db:db_dependency,todo_id: int= Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id==todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404,detail='Todo not found')
#
#     db.query(Todos).filter(Todos.id==todo_id).delete()
#
#     db.commit()

@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()

    db.commit()





# app.include_router(auth.router)
# app.include_router(todos.router)
# app.include_router(admin.router)
# app.include_router(users.router)