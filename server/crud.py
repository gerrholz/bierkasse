from sqlalchemy.orm import Session

from . import models, schemas, utils

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_card(db: Session, card_id: str):
    return db.query(models.User).filter(models.User.cards.any(id=card_id)).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=utils.get_password_hash(user.password), display_name=user.display_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user