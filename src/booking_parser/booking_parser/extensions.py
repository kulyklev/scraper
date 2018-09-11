from threading import Timer
from datetime import datetime, timedelta
from scrapy.exceptions import NotConfigured
from scrapy import signals
from helpers.db_helper import DBHelper
import scrapy
import time
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
        self.channel.basic_consume(self.rabbit_callback, queue='task_queue')

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('ENDLESS_SPIDER_EXT_ENABLED'):
            raise NotConfigured

        ext = cls(crawler)
        crawler.signals.connect(ext.idle, signal=signals.spider_idle)

        return ext

    def idle(self, spider):
        self.channel.start_consuming()

    def create_request(self, data):
        link = data[0].decode("utf-8")
        checkin_date = data[1].decode("utf-8")
        checkout_date = datetime.strptime(checkin_date, '%Y-%m-%d') + timedelta(days=1)

        url = link + '?' + 'checkin=' + checkin_date + ';checkout=' + str(checkout_date.date())

        r = scrapy.Request(url=url, callback=self.crawler.spider.parse_hotel, headers=self.crawler.spider.hdrs)

        return r

    def rabbit_callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)
        data = body.split()
        self.crawler.engine.crawl(self.create_request(data=data), self.crawler.spider)
        self.channel.stop_consuming()
        print(" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag)
