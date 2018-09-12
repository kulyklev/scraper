import argparse
import json
import os
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings


parser = argparse.ArgumentParser()
parser.add_argument("filename", help="The name of json file with data")
args = parser.parse_args()

with open(args.filename) as f:
    data = json.load(f)
os.remove(args.filename)

settings = get_project_settings()
process = CrawlerProcess(settings)

for arg in data:
    if arg['concurrent_request_amount'] is not None:
        settings['CONCURRENT_REQUESTS'] = arg['concurrent_request_amount']
        process = CrawlerProcess(settings)
    process.crawl('booking', kwargs=arg)

process.start()