from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True)
    password = Column(String(200))

    portfolios = relationship("Portfolio", back_populates="owner")


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    linkedin = Column(String(200))
    github = Column(String(200))

    summary = Column(Text)
    education = Column(Text)
    experience = Column(Text)

    role = Column(String(100))
    projects = Column(Text)
    image_path = Column(String(200))

    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="portfolios")