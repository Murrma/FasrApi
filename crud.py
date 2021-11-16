from sqlalchemy.orm import Session

import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.User):
    db_user = models.User(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_client(db: Session, user: schemas.User):
    test_client = db.query(models.User).get(user.id)
    for attr in list(user.dict().keys()):
        setattr(test_client, attr, user.dict()[attr])
        db.flush()
    db.commit()


def delete_user(db: Session, user: schemas.User):
    db.delete(db.query(models.User).filter(models.User.id == user.id).first())
    db.commit()
    db.delete(db.query(models.Item).filter(models.Item.owner_id == user.id).all())
    db.commit()


######################################


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_item(db: Session, order_id: int):
    return db.query(models.Item).get(order_id)


def create_user_item(db: Session, item: schemas.Item):
    db_item = models.Item(item.title, item.description, item.owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
