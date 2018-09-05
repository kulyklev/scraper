import argparse
import json
import os
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from booking_parser.spiders.booking_spider import BookingSpider
from twisted.internet import reactor, defer


parser = argparse.ArgumentParser()
parser.add_argument("filename", help="The name of json file with data")
args = parser.parse_args()

with open(args.filename) as f:
    data = json.load(f)
os.remove(args.filename)

process = CrawlerProcess(get_project_settings())
for arg in data:
    process.crawl('booking', kwargs=arg)
process.start()