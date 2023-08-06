from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # The username must be unique
    username = Column(String, unique=True, index=True)
    # The display name
    display_name = Column(String)
    # The password is hashed
    password = Column(String)
    # The balance of the user
    balance = Column(Float, default=0.0)
    disabled = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)

    # The cards that belong to this user
    cards = relationship("Card", back_populates="user")


# A card is used to represent one student card. It is linked to a user.
class Card(Base):
    __tablename__ = "cards"

    id = Column(String, primary_key=True, index=True)
    # The user that owns this card
    user_id = Column(Integer, ForeignKey("users.id"))

    # The user that owns this card
    user = relationship("User", back_populates="cards")