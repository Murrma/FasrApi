from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.UserBase)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.patch('/users/', response_model=schemas.User)
def change_user(user: schemas.User, db: Session = Depends(get_db)):
    try1 = crud.get_user(db, user_id=user.id)
    if try1:
        return crud.update_client(db, user=user)
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.delete('/users/{user_id}')
def del_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db, user_id=user_id)


#################################################


@app.post("/users/{user_id}/items/", response_model=schemas.ItemBase)
def create_item_for_user(
        item: schemas.ItemBase, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.get('/items/{item_id}')
def read_item(item_id: int, db: Session = Depends(get_db)):
    return crud.get_item(db, item_id)


@app.delete('/items/del/{item_id}')
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_user(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.delete_item(db, item_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host="127.0.0.1")
