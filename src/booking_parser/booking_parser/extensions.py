from scrapy.exceptions import NotConfigured
from scrapy import signals
from helpers.db_helper import DBHelper
from scrapy.exceptions import CloseSpider


class SpiderState(object):
    def __init__(self, crawler):
        self.current_state = 0
        self.db = DBHelper()
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured

        ext = cls(crawler)
        # TODO Remove signal connection. Replace it with timer
        crawler.signals.connect(ext.pause_spider, signal=signals.item_scraped)

        return ext

    def change_spider_state(self):
        spider_conf = self.db.select_spider_state(1)
        self.current_state += 1

        # print("Id: " + str(model.id))
        # print("State: " + str(model.state))

    def pause_spider(self):
        self.crawler.engine.pause()
        print("Spider paused.")

    def resume_spider(self):
        self.crawler.engine.unpause()
        print("Spider resumed.")

    def stop_spider(self):
        raise CloseSpider("Spider stopped by userr command.")

        # TODO compare current_state with state from db
        # TODO skip if states are equal. Do sth if states are different
