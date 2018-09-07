from threading import Timer
from scrapy.exceptions import NotConfigured
from scrapy import signals
from helpers.db_helper import DBHelper


class SpiderState(object):
    def __init__(self, crawler):
        self.current_state = None
        self.db = DBHelper()
        self.crawler = crawler
        self.t = None

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured

        ext = cls(crawler)

        crawler.signals.connect(ext.run_state_checker, signal=signals.engine_started)
        crawler.signals.connect(ext.stop_state_checker, signal=signals.spider_closed)

        return ext

    def run_state_checker(self):
        if self.crawler is not None:
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
