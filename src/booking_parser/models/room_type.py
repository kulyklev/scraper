from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER

Base = declarative_base()


class RoomType(Base):
    __tablename__ = 'room_types'

    id = Column('id', INTEGER(unsigned=True), primary_key=True, nullable=False)
    hotel_id = Column('hotel_id', INTEGER(unsigned=True), nullable=False)
    name = Column('type', String(300))
    photo = Column('photo', String(100))