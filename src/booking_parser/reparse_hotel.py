from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

settings['ENDLESS_SPIDER_EXT_ENABLED'] = True

process = CrawlerProcess(settings)
process.crawl("booking_reparse")
process.start()