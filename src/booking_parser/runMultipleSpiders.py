import argparse
import json
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from booking_parser.spiders.booking_spider import BookingSpider
from twisted.internet import reactor, defer


parser = argparse.ArgumentParser()
parser.add_argument("jsonnn", type=json.dumps)
args = parser.parse_args()


process = CrawlerProcess(get_project_settings())
for arg in json.loads(json.loads(args.jsonnn)):
    process.crawl('booking', kwargs=arg)
process.start()