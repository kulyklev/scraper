# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelItem(scrapy.Item):

    hotel_id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    description = scrapy.Field()
    rate = scrapy.Field()
    stars = scrapy.Field()
    rooms = scrapy.Field()

    photo_url = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    pass


class RoomTypeItem(scrapy.Item):
    id = scrapy.Field()
    hotel_id = scrapy.Field()
    name = scrapy.Field()
    image_url = scrapy.Field()
    room_items = scrapy.Field()
    pass


class RoomItem(scrapy.Item):
    room_type_id = scrapy.Field()
    price = scrapy.Field()
    date = scrapy.Field()
    sleeps = scrapy.Field()
    pass

