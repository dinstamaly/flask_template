# coding=utf-8
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

__author__ = 'Din'


db = SQLAlchemy()
Base = db.Model


class User(Base):
    __tablename__ = 't_user'
    __table_args__ = {u'schema': 'service'}

    id = Column(Integer, primary_key=True)
    f_username = Column(String(64), nullable=False, unique=True)
    f_password = Column(String(64))
    f_name = Column(String(64), default='')
    f_phone = Column(String(64), default='')
    f_email = Column(String(128), default='')
    f_position = Column(String(256), default='')
    f_date_create = Column(DateTime, default=datetime.now())
    f_blocked = Column(Boolean, default=False)


class Device(Base):
    __tablename__ = 't_device'
    __table_args__ = {"schema": "service"}

    id = Column(Integer, primary_key=True)
    f_user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    f_device_id = Column(String(128))
    f_device_name = Column(String(128))
    f_language = Column(String(2))
    f_token = Column(String(128))
    f_date = Column(DateTime)
    user = relationship(User)

