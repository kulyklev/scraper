from threading import Timer
from datetime import datetime, timedelta
from scrapy.exceptions import NotConfigured, DontCloseSpider
from scrapy import signals
from helpers.db_helper import DBHelper
import scrapy
import pika


class SpiderState(object):
    def __init__(self, crawler):
        self.current_state = None
        self.db = DBHelper()
        self.crawler = crawler
        self.t = None

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('SPIDER_STATE_EXT_ENABLED'):
            raise NotConfigured

        ext = cls(crawler)

        crawler.signals.connect(ext.run_state_checker, signal=signals.engine_started)
        crawler.signals.connect(ext.stop_state_checker, signal=signals.spider_closed)

        return ext

    def run_state_checker(self):
        if self.crawler.crawling is not False:
            self.t = Timer(5.0, self.change_spider_state)
            self.t.start()

    def stop_state_checker(self):
        self.t.cancel()

    def change_spider_state(self):
        spider_conf = self.db.select_spider_state(self.crawler.spider.config_id)

        self.crawler.spider.logger.info(
            "\nSpider id: {0}\nSpider state: {1}".format(str(self.crawler.spider.config_id), str(spider_conf.state)))

        if spider_conf.state != self.current_state:
            self.current_state = spider_conf.state

            if spider_conf.state == 1:
                self.pause_spider()
                self.run_state_checker()
            elif spider_conf.state == 2:
                self.resume_spider()
                self.run_state_checker()
            elif spider_conf.state == 3:
                self.stop_spider()
            else:
                self.run_state_checker()
        else:
            self.run_state_checker()

    def pause_spider(self):
        self.crawler.engine.pause()
        self.current_state = 1
        print("Spider paused.")

    def resume_spider(self):
        self.crawler.engine.unpause()
        self.current_state = 2
        print("Spider resumed.")

    def stop_spider(self):
        self.current_state = 3
        self.crawler.stop()


class EndlessSpider(object):
    def __init__(self, crawler):
        self.crawler = crawler

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='task_queue', durable=True)
        self.channel.basic_qos(prefetch_count=1)

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('ENDLESS_SPIDER_EXT_ENABLED'):
            raise NotConfigured

        ext = cls(crawler)

        crawler.signals.connect(ext.idle, signal=signals.spider_idle)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        return ext

    def idle(self, spider):
        self.schedule_next_request()
        raise DontCloseSpider

    def schedule_next_request(self):
        req = self.next_request()

        if req:
            self.crawler.engine.crawl(req, spider=self.crawler.spider)

    def next_request(self):
        method_frame, header_frame, data = self.channel.basic_get(queue='task_queue')

        if data:
            data = data.split()
            link = data[0].decode("utf-8")
            checkin_date = data[1].decode("utf-8")
            checkout_date = datetime.strptime(checkin_date, '%Y-%m-%d') + timedelta(days=7)

            url = link + '?' + 'checkin=' + checkin_date + ';checkout=' + str(checkout_date.date())
            self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            return self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        return scrapy.Request(url=url, callback=self.crawler.spider.parse_hotel, headers=self.crawler.spider.hdrs)

    def item_scraped(self):
        self.schedule_next_request()
