from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, SmallInteger
from sqlalchemy.dialects.mysql import INTEGER

Base = declarative_base()


class StartConfig(Base):
    __tablename__ = 'spider_start_config'

    id = Column('id', INTEGER(unsigned=True), primary_key=True, nullable=False)
    country = Column('country', String(128))
    city = Column('city', String(128))
    checkin_date = Column('checkin_date', String(64))
    checkout_date = Column('checkout_date', String(64))
    vpn = Column('vpn', Boolean, default=False)
    concurrent_request_amount = Column('concurrent_request_amount', SmallInteger)
    state = Column('state', SmallInteger, comment='1 - pause, 2 - stop, other values - run', default=0)