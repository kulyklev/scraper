import logging
import scrapy
from scrapy.spiders import CrawlSpider
from booking_parser.items import HotelItem
from booking_parser.items import RoomTypeItem
from booking_parser.items import RoomItem
from helpers.db_helper import DBHelper
from datetime import datetime, timedelta


class BookingSpider(CrawlSpider, DBHelper):
    name = "booking"
    config_id = None

    hdrs = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                  'image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }

    allowed_domains = ['www.booking.com']
    start_urls = [

    ]

    def __init__(self, *args, **kwargs):
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        logging.getLogger('').addHandler(console)

        self.arguments = kwargs.get('kwargs')
        self.use_vpn = self.arguments['use_vpn']
        self.vpn_response_error_counter = 0
        self.config_id = self.arguments.get('config_id', None)

        super().__init__(*args, **kwargs)

    def start_requests(self):
        checkin_date = self.arguments['check_in_date']
        checkout_date = datetime.strptime(checkin_date, '%Y-%m-%d') + timedelta(days=1)
        url = self.arguments['hotel_link'] + '?' + 'checkin=' + self.arguments['check_in_date'] + ';checkout=' + str(checkout_date.date())

        return [scrapy.Request(url=url, callback=self.parse_hotel, headers=self.hdrs)]

        # return [scrapy.FormRequest(
        #     url="https://www.booking.com/searchresults.ru.html?id=test",
        #     method="GET",
        #     formdata={
        #         'ss': self.arguments['country'] + ' ' + self.arguments['city'],
        #         'checkin_monthday': str(self.arguments['checkin_monthday']),
        #         'checkin_month': str(self.arguments['checkin_month']),
        #         'checkin_year': str(self.arguments['checkin_year']),
        #
        #         'checkout_monthday': str(self.arguments['checkout_monthday']),
        #         'checkout_month': str(self.arguments['checkout_month']),
        #         'checkout_year': str(self.arguments['checkout_year']),
        #     },
        #     callback=self.parse,
        #     headers=self.hdrs
        # )]

    def parse(self, response):
        for link in response.xpath("//div[@id='hotellist_inner']//div[@class='sr-cta-button-row']/a"):
            hotel_page_href = link.css('a::attr(href)').extract_first().strip()
            hotel_page = response.urljoin(hotel_page_href)
            yield scrapy.Request(hotel_page, callback=self.parse_hotel,
                                 headers=self.hdrs)

        next_page = response.xpath("//li[contains(@class,'bui-pagination__item bui-pagination__next-arrow')]/a/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse,
                                 headers=self.hdrs)

    def parse_hotel(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        hotel = HotelItem()
        hotel['hotel_id'] = response.xpath("//form[@id='top-book']/input[@name='hotel_id']/@value").extract_first()
        hotel['url'] = response.url[:response.url.find('?')]
        hotel['name'] = response.xpath("//h2[@class='hp__hotel-name']/text()").extract_first().strip()
        hotel['description'] = " ".join(response.xpath("//div[@id='summary']/p/text()").extract()).strip()
        hotel['address'] = response.xpath(
            "//span[contains(@class, 'hp_address_subtitle')]/text()").extract_first().strip()
        hotel['rate'] = response.css(
            "span.review-score-widget__auto > span.review-score-badge::text").extract_first()

        image = response.xpath("//div[@id='photos_distinct']/a[1] | "
                               "//a[contains(@class,'bh-photo-grid-photo1')]")
        hotel['image_urls'] = image.xpath("@href").extract()
        hotel['photo_url'] = image.xpath("@href").extract_first()

        checkin_date = response.xpath("//form[@id='top-book']/input[@name='checkin']/@value").extract_first()
        raw_rooms = self.get_raw_rooms(response)
        parsed_rooms = self.get_parsed_rooms(raw_rooms, hotel['hotel_id'], checkin_date)
        hotel['rooms'] = parsed_rooms

        for room_type in parsed_rooms:
            if room_type['image_url'] is not None:
                hotel['image_urls'].append(room_type['image_url'])

        yield hotel

    # Method get_rooms accepts response and finds all rows(tr tags) which belongs to one room type and selects external
    # data about room.
    # Then return 2D array, where each row represents one room type and contoinas all trs which bellong to it
    def get_raw_rooms(self, response):
        rooms = []
        room_types = []

        for row in response.xpath("//form[@id='hprt-form']/table[contains(@class, 'hprt-table')]/tbody/tr"):
            class_list = row.xpath("@class").extract_first()
            data_block_id = row.xpath("@data-block-id").extract_first()

            if data_block_id is not '' and class_list.find('hprt-cheapest-block-row') is not 1:
                if class_list.find("hprt-table-last-row ") is not -1:
                    rooms.append(row)
                    room_id = row.xpath(".//select[@class='hprt-nos-select']/@data-room-id").extract_first()
                    room_details = response.xpath("//div[@data-room-id='" + room_id + "']")
                    room_data = {
                        'room_details': room_details,
                        'rooms': rooms
                    }
                    room_types.append(room_data)
                    rooms = []
                else:
                    rooms.append(row)

        return room_types

    def get_parsed_rooms(self, raw_rooms, h_id, checkin_date):
        result = []

        for rooms_data in raw_rooms:
            raw_room = rooms_data['rooms']

            room_type_item = RoomTypeItem()
            room_type_item['id'] = raw_room[0].xpath(
                ".//select[@class='hprt-nos-select']/@data-room-id").extract_first()
            room_type_item['hotel_id'] = h_id
            room_type_item['name'] = raw_room[0].xpath(
                ".//a[contains(@class,'hprt-roomtype-link')]/@data-room-name").extract_first()
            room_type_item['image_url'] = self.get_photo_url(rooms_data['room_details'])
            room_type_item['room_items'] = []

            for tr in raw_room:
                room_item = RoomItem()
                room_item['price'] = tr.xpath(
                    ".//div[contains(@class,'hprt-price-price')]/span/text()").extract_first()

                if room_item['price'] is not None:
                    room_item['room_type_id'] = room_type_item['id']
                    room_item['price'] = room_item['price'].strip()
                    room_item['date'] = checkin_date
                    room_item['sleeps'] = tr.xpath(
                        "count( .//div[contains(@class,'hprt-occupancy-occupancy-info')]/i )").extract_first()

                    room_type_item['room_items'].append(room_item)

            result.append(room_type_item)

        return result

    def get_photo_url(self, room_details):
        photo_id = room_details.xpath(
            ".//div[@class='b_nha_hotel_small_images']//a/@data-photoid").extract_first()

        if photo_id is not None:
            photo_url = room_details.xpath("//a[@data-photoid='" + photo_id + "']/@href | "
                                           "//div[@data-photoid='" + photo_id + "']/img/@data-lazy").extract_first()
        else:
            photo_url = None

        return photo_url
