from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum as BaseEnum
from datetime import datetime


base_table = declarative_base()


class TypeUser(int, BaseEnum):
    USER = 1
    CHECKER = 2
    ADMIN = 3


class User(base_table):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    surname = Column(String(32), nullable=False)
    patronymic = Column(String(32), nullable=False)

    is_activ = Column(Boolean, default=False)

    type_user = Column(Enum(TypeUser), default=TypeUser.USER)

    last_activ = Column(DateTime, default=datetime.now())
    is_online = Column(Boolean, default=False)

    login = Column(String(50), nullable=False)
    hash_password = Column(String, nullable=False, name="password")

    @property
    def password(self):
        return self.hash_password

    @password.setter
    def password(self, val):
        self.hash_password = generate_password_hash(val)

    def check_password(self, password):
        return check_password_hash(self.password, password)
