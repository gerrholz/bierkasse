from pydantic import BaseModel

class Card(BaseModel):
    id: str
    user_id: int

    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    username: str
    display_name: str
    password: str
    balance: float
    disabled: bool
    admin: bool

    cards : list[Card] = []

    class Config:
        orm_mode = True


# This is used for jwt authentication
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
