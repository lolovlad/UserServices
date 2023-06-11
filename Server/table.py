from sqlalchemy import Column, Integer, String, Boolean, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum as BaseEnum
from datetime import datetime


base_table = declarative_base()


class TypeUser(int, BaseEnum):
    USER = 1
    CHECKER = 2
    ADMIN = 3


class Country(base_table):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_country = Column(String, nullable=False)
    additional_information = Column(JSONB, nullable=True)


class City(base_table):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_country = Column(Integer, ForeignKey("countries.id"), nullable=False)
    name_city = Column(String(32), nullable=False)
    additional_information = Column(JSONB, nullable=True)


class Role(base_table):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_role = Column(String(12), nullable=False, default="user")


class User(base_table):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    login = Column(String(50), nullable=False)
    hash_password = Column(String, nullable=False, name="password")
    role_id = Column(Integer, ForeignKey("roles.id"))

    name = Column(String(32), nullable=False)
    surname = Column(String(32), nullable=False)
    patronymic = Column(String(32), nullable=False)

    email = Column(String(64), nullable=False)
    phone = Column(String(24), nullable=False)

    country_id = Column(Integer, ForeignKey("countries.id"))
    city_id = Column(Integer, ForeignKey("cities.id"))

    registered_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    is_active = Column(Boolean, default=False)

    additional_information = Column(JSONB, nullable=True)

    role = relationship('Role', join_depth=1, back_populates="roles", lazy="joined")
    country = relationship('Country', join_depth=1, back_populates="countries", lazy="joined")
    city = relationship('City', join_depth=1, back_populates="cities", lazy="joined")

    @property
    def password(self):
        return self.hash_password

    @password.setter
    def password(self, val):
        self.hash_password = generate_password_hash(val)

    def check_password(self, password):
        return check_password_hash(self.password, password)
