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

# data = [
#     {
#         "config_id": 1,
#         "city": "Los-Angeles",
#         "country": "USA",
#         "checkin_monthday": 12,
#         "checkin_month": 12,
#         "checkin_year": 2018,
#
#         "checkout_monthday": 13,
#         "checkout_month": 12,
#         "checkout_year": 2018,
#
#         "use_vpn": False,
#     },
#
#     {
#         "config_id": 2,
#         "city": "Las-Vegas",
#         "country": "USA",
#         "checkin_monthday": 12,
#         "checkin_month": 12,
#         "checkin_year": 2018,
#
#         "checkout_monthday": 13,
#         "checkout_month": 12,
#         "checkout_year": 2018,
#
#         "use_vpn": False,
#     },
#
#     {
#         "config_id": 2,
#         "city": "Никополь",
#         "country": "Украина",
#         "checkin_monthday": 12,
#         "checkin_month": 12,
#         "checkin_year": 2018,
#
#         "checkout_monthday": 13,
#         "checkout_month": 12,
#         "checkout_year": 2018,
#
#         "use_vpn": False,
#     }
# ]

process = CrawlerProcess(get_project_settings())
for arg in data:
    process.crawl('booking', kwargs=arg)
process.start()