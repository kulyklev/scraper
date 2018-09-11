import argparse
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from helpers.validator import Validator


# Setting up argparse
# parser = argparse.ArgumentParser()
# parser.add_argument("hotel_link", help="Entry hotel link from booking.com")
# parser.add_argument("check_in_date", help="Check-in date format YYYY-MM-DD")
# parser.add_argument("--vpn", help="Using this flag cause parsing through vpn", action="store_true")
# parser.add_argument("-r", "--requests", help="The maximum number of concurrent requests that will be performed by the "
#                                              "Scrapy downloader.", type=int)
#
# args = parser.parse_args()
# kwargs = {
#         'hotel_link': args.hotel_link,
#         'check_in_date': args.check_in_date,
#
#         'use_vpn': args.vpn,
#     }
#
#
# settings = get_project_settings()

# if args.requests is not None:
#     settings['CONCURRENT_REQUESTS'] = args.requests
#     process = CrawlerProcess(settings)
# else:
#     process = CrawlerProcess(get_project_settings())

process = CrawlerProcess(get_project_settings())
process.crawl('booking')
process.start()