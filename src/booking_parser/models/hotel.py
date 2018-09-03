from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, SmallInteger
from sqlalchemy.dialects.mysql import INTEGER

Base = declarative_base()


class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column('id', INTEGER(unsigned=True), primary_key=True, nullable=False)
    url = Column('url', String(2000))
    name = Column('name', String(200))
    address = Column('address', String(250))
    description = Column('description', Text)
    rate = Column('rate', SmallInteger)
    photo = Column('photo', String(100))
    # stars = Column('stars', SmallInteger)
