from sqlalchemy.orm import Session

from . import models, schemas, utils

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

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

def increase_balance(db: Session, user: schemas.User, amount: int):
    user.balance += amount
    db.commit()
    db.refresh(user)
    return user

def decrease_balance(db: Session, user: schemas.User, amount: int):
    user.balance -= amount
    db.commit()
    db.refresh(user)
    return user

def create_user_card(db: Session, user: schemas.User, card: schemas.Card):
    db_card = models.Card(id=card.id, user_id=user.id)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def delete_card(db: Session, user: schemas.User, card: schemas.Card):
    db.delete(card)
    db.commit()
    return card

def get_cards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Card).offset(skip).limit(limit).all()

def get_card(db: Session, card_id: str):
    return db.query(models.Card).filter(models.Card.id == card_id).first()