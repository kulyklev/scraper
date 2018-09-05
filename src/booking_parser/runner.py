import argparse
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from helpers.validator import Validator


# Setting up argparse
parser = argparse.ArgumentParser()
parser.add_argument("country", help="Entry country where you want to go")
parser.add_argument("city", help="Entry city where you want to go")
parser.add_argument("check_in_date", help="Check-in date format YYYY-MM-DD")
parser.add_argument("check_out_date", help="Check-out date format YYYY-MM-DD")
parser.add_argument("--vpn", help="Using this flag cause parsing through vpn", action="store_true")
parser.add_argument("-r", "--requests", help="The maximum number of concurrent requests that will be performed by the "
                                             "Scrapy downloader.", type=int)

args = parser.parse_args()

validator = Validator()
if validator.validate_input(checkin_date=args.check_in_date, checkout_date=args.check_out_date):
    c_in = datetime.strptime(args.check_in_date, '%Y-%m-%d')
    c_out = datetime.strptime(args.check_out_date, '%Y-%m-%d')

    kwargs = {
        'country': args.country,
        'city': args.city,
        'checkin_monthday': c_in.day,
        'checkin_month': c_in.month,
        'checkin_year': c_in.year,

        'checkout_monthday': c_out.day,
        'checkout_month': c_out.month,
        'checkout_year': c_out.year,

        'use_vpn': args.vpn,
    }

    # Starting scrapy
    if args.requests is not None:
        settings = get_project_settings()
        settings['CONCURRENT_REQUESTS'] = args.requests
        process = CrawlerProcess(settings)
        process.crawl('booking', kwargs=kwargs)
        process.start()
    else:
        process = CrawlerProcess(get_project_settings())
        process.crawl('booking', kwargs=kwargs)
        process.start()
