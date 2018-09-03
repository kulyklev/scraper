from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER

Base = declarative_base()


class Room(Base):
    __tablename__ = 'rooms'

    id = Column('id', INTEGER(unsigned=True), primary_key=True, autoincrement=True, nullable=False)
    room_type_id = Column('room_type_id', INTEGER(unsigned=True), nullable=False)
    price = Column('price', String(100))
    date = Column('date', String(100))
    sleeps = Column('sleeps', Integer)