from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import crud, schemas, auth, dependencies

app = FastAPI()

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(dependencies.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = auth.timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db), current_user: schemas.User = Depends(auth.get_current_active_superuser)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_active_user)):
    return current_user


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(dependencies.get_db), current_user: schemas.User = Depends(auth.get_current_active_superuser)):
    db_user = crud.get_user(db, user_id=user_id)
    return db_user


@app.get("/balance/increase", response_model=schemas.User)
def increase_balance(amount: int, db: Session = Depends(dependencies.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    return crud.increase_balance(db, user=current_user, amount=amount)

@app.get("/balance/decrease", response_model=schemas.User)
def decrease_balance(amount: int, db: Session = Depends(dependencies.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    return crud.decrease_balance(db, user=current_user, amount=amount)


@app.get("/cards/", response_model=list[schemas.Card]) 
def read_cards(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    cards = crud.get_cards(db, skip=skip, limit=limit)
    return cards

# Only admins can create cards for security reasons
@app.post("/user/{user_id}/cards/", response_model=schemas.Card)
def create_card_for_user(user_id: int, card: schemas.CardCreate, db: Session = Depends(dependencies.get_db), current_user: schemas.User = Depends(auth.get_current_active_superuser)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not registered")
    db_card = crud.get_user_by_card(db, card_id=card.id)
    if db_card:
        raise HTTPException(status_code=400, detail="Card already registered")
    return crud.create_user_card(db=db, card=card, user=db_user)

@app.delete("/cards/{card_id}", response_model=schemas.Card)
def delete_card(card_id: str, db: Session = Depends(dependencies.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    db_card = crud.get_card(db, card_id=card_id)
    if not db_card:
        raise HTTPException(status_code=400, detail="Card not registered")
    if db_card.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Card does not belong to user")
    return crud.delete_card(db=db, user=current_user, card=db_card)
