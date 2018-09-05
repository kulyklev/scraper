import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import load_only
from scrapy.utils.project import get_project_settings
from models.start_config import StartConfig


class DBHelper:
    settings = get_project_settings()
    engine = create_engine(settings.get("DB_CONNECTION_STRING"))
    session = Session(engine)

    def store_hotel(self, hotel):
        try:
            self.session.merge(hotel)
            self.session.commit()
        except SQLAlchemyError as error:
            self.session.rollback()
            logging.error(error)

    def store_room_types(self, room_types):
        try:
            for room_type in room_types:
                self.session.merge(room_type)
            self.session.commit()
        except SQLAlchemyError as error:
            self.session.rollback()
            logging.error(error)

    def store_rooms(self, room):
        try:
            self.session.bulk_save_objects(room)
            self.session.commit()
        except SQLAlchemyError as error:
            self.session.rollback()
            logging.error(error)

    def select_run_configs(self):
        res = None
        try:
            res = self.session.query(StartConfig).all()
        except SQLAlchemyError as error:
            self.session.rollback()
            logging.error(error)
        return res

    def select_spider_state(self, spider_id):
        res = None
        try:
            res = self.session.query(StartConfig).filter(StartConfig.id == spider_id).options(load_only("state")).first()
            self.session.commit()
        except SQLAlchemyError as error:
            self.session.rollback()
            logging.error(error)
        return res