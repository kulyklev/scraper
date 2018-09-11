# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import pprint
import json
import pika

from models.hotel import Hotel
from models.room_type import RoomType
from models.room import Room
from scrapy.mail import MailSender
from scrapy.utils.project import get_project_settings


class HotelPipeline(object):

    def close_spider(self, spider):
        spider.logger.log(45, spider.crawler.stats.get_stats())
        # TODO Uncomment
        # self.send_email(spider.crawler.stats.get_stats())

    def send_email(self, stats):
        intro = "Summary stats from Scrapy spider: \n\n"
        body = stats
        body = pprint.pformat(body)
        body = intro + body

        settings = get_project_settings()
        mailer = MailSender(smtphost=settings.get("SMTP_HOST"),
                            mailfrom=settings.get("MAIL_FROM"),
                            smtpuser=settings.get("SMTP_USER"),
                            smtppass=settings.get("SMTP_PASS"),
                            smtpport=settings.get("SMTP_PORT"),
                            smtptls=settings.get("SMTP_TLS"),
                            smtpssl=settings.get("SMTP_SSL")
                            )
        mailer.send(to=settings.get("MAIL_RECEIVERS"),
                    subject="Booking Scrapy parser. Report for " + datetime.datetime.today().strftime("%d.%m.%Y %H:%M"),
                    body=body,
                    )

    def process_item(self, item, spider):
        img = None

        for image in item['images']:
            if image['url'] == item['photo_url']:
                img = image
                break

        if item['rate'] is None:
            item['rate'] = 0.0
        else:
            item['rate'] = item['rate'].replace(',', '.')
            item['rate'] = float(item['rate'])

        hotel = Hotel(
            id=item['hotel_id'],
            url=item['url'],
            name=item['name'],
            address=item['address'],
            description=item['description'],
            rate=item['rate'],
            photo=img['path'],
            # stars=item['stars'],
        )
        spider.store_hotel(hotel)

        item = {
            'rooms': item['rooms'],
            'photos': item['images']
        }

        return item


class RoomTypePipeline(object):
    def process_item(self, item, spider):
        room_types = item['rooms']
        photos = item['photos']
        img = None
        rooms = []
        room_type_models = []

        for room_type in room_types:
            for photo in photos:
                if photo['url'] == room_type['image_url']:
                    img = photo
                    break

            if img is None:
                new_room_type = RoomType(
                    id=room_type['id'],
                    hotel_id=room_type['hotel_id'],
                    name=room_type['name'],
                )
            else:
                new_room_type = RoomType(
                    id=room_type['id'],
                    hotel_id=room_type['hotel_id'],
                    name=room_type['name'],
                    photo=img['path'],
                )
            room_type_models.append(new_room_type)

            rooms = [room for room in room_type['room_items']]

        spider.store_room_types(room_type_models)

        return rooms


class RoomPipeline(object):
    def process_item(self, item, spider):
        room_models = []

        for room in item:
            new_room = Room(
                room_type_id=room['room_type_id'],
                price=room['price'],
                sleeps=room['sleeps'],
                date=room['date'],
            )
            room_models.append(new_room)

        spider.store_rooms(room_models)

        return item


class HotelPipelineJSON(object):

    def close_spider(self, spider):
        spider.logger.log(45, spider.crawler.stats.get_stats())
        # TODO Uncomment
        # self.send_email(spider.crawler.stats.get_stats())

    def send_email(self, stats):
        intro = "Summary stats from Scrapy spider: \n\n"
        body = stats
        body = pprint.pformat(body)
        body = intro + body

        settings = get_project_settings()
        mailer = MailSender(smtphost=settings.get("SMTP_HOST"),
                            mailfrom=settings.get("MAIL_FROM"),
                            smtpuser=settings.get("SMTP_USER"),
                            smtppass=settings.get("SMTP_PASS"),
                            smtpport=settings.get("SMTP_PORT"),
                            smtptls=settings.get("SMTP_TLS"),
                            smtpssl=settings.get("SMTP_SSL")
                            )
        mailer.send(to=settings.get("MAIL_RECEIVERS"),
                    subject="Booking Scrapy parser. Report for " + datetime.datetime.today().strftime("%d.%m.%Y %H:%M"),
                    body=body,
                    )

    def process_item(self, item, spider):
        img = None

        for image in item['images']:
            if image['url'] == item['photo_url']:
                img = image
                break

        if item['rate'] is None:
            item['rate'] = 0.0
        else:
            item['rate'] = item['rate'].replace(',', '.')
            item['rate'] = float(item['rate'])

        hotel = {
            'id': item['hotel_id'],
            'url': item['url'],
            'name': item['name'],
            'address': item['address'],
            'description': item['description'],
            'rate': item['rate'],
            'photo': img['path'],
            'room_types': self.get_room_types(item['rooms'], item['images'])
        }

        self.sendToRabbit(hotel)

        return item

    def get_room_types(self, rooms, photos):
        room_types = rooms
        photos = photos
        img = None
        room_type_models = []

        for room_type in room_types:
            for photo in photos:
                if photo['url'] == room_type['image_url']:
                    img = photo
                    break

            if img is None:
                new_room_type = {
                    'id': room_type['id'],
                    'hotel_id': room_type['hotel_id'],
                    'name': room_type['name'],
                    'rooms': self.get_rooms(room_type['room_items'])
                }
            else:
                new_room_type = {
                    'id': room_type['id'],
                    'hotel_id': room_type['hotel_id'],
                    'name': room_type['name'],
                    'photo': img['path'],
                    'rooms': self.get_rooms(room_type['room_items'])
                }

            room_type_models.append(new_room_type)

        return room_type_models

    def get_rooms(self, room_items):
        room_models = []

        for room in room_items:
            new_room = {
                'room_type_id': room['room_type_id'],
                'price': room['price'],
                'sleeps': room['sleeps'],
                'date': room['date'],
            }
            room_models.append(new_room)

        return room_models

    def sendToRabbit(self, hotel):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
        channel = connection.channel()

        channel.queue_declare(queue='save_data_queue', passive=False, durable=True, exclusive=False, auto_delete=False)

        message = json.dumps(hotel)
        channel.basic_publish(body=message, exchange='', routing_key='save_data_queue')
        print(" [x] Sent data to RabbitMQ")
        connection.close()