import time
from multiprocessing import Pool
from scrapy.exceptions import NotConfigured
from scrapy import signals
from helpers.db_helper import DBHelper
from scrapy.exceptions import CloseSpider

# TODO Write function which will check spider state in separate process or thread or whatever


class SpiderState(object):
    def __init__(self, crawler):
        self.current_state = None
        self.db = DBHelper()
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured

        ext = cls(crawler)

        crawler.signals.connect(ext.run_state_checker_process, signal=signals.engine_started)

        # ext.change_spider_state()

        # TODO Maybe use timer

        return ext

    def run_state_checker_process(self):
        with Pool(processes=1) as pool:
            pool.apply_async(self.state_checker())

    def state_checker(self):
        while True:
            self.change_spider_state()
            print("LALALALALALa")
            time.sleep(5)

    def change_spider_state(self):
        # TODO Pass to select_spider_state conf id
        spider_conf = self.db.select_spider_state(1)

        print(spider_conf.state)

        if spider_conf.state != self.current_state:
            self.current_state = spider_conf.state

            if spider_conf.state == 1:
                self.pause_spider()
            elif spider_conf.state == 2:
                self.resume_spider()
            elif spider_conf.state == 3:
                self.stop_spider()

    def pause_spider(self):
        self.crawler.engine.pause()
        print("Spider paused.")

    def resume_spider(self):
        self.crawler.engine.unpause()
        print("Spider resumed.")

    def stop_spider(self):
        raise CloseSpider("Spider stopped by user command.")
