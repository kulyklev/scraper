# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import pprint
from datetime import datetime

from scrapy import signals
from scrapy.mail import MailSender
from scrapy.utils.project import get_project_settings


class BookingParserSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BookingParserDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        if spider.use_vpn:
            settings = get_project_settings()
            request.meta['proxy'] = settings.get("PROXY_CONFIG")

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

        if spider.use_vpn:
            if response.status == 407:
                spider.vpn_response_error_counter += 1
                spider.logger.error("VPN. 407 error")

            if response.status == 429:
                spider.vpn_response_error_counter += 1
                spider.logger.error("VPN. 429 error")

            if spider.vpn_response_error_counter == 10:
                self.send_email()

        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def send_email(self):
        intro = "407 and 429 errors: \n\n"
        body = "During current parsing session received 10 responses with status 407 or 429"
        body = pprint.pformat(body)
        body = intro + body

        settings = get_project_settings()
        mailer = MailSender(smtphost=settings.get("SMTP_HOST"),
                            mailfrom=settings.get("MAIL_FROM"),
                            smtpuser=settings.get("SMTP_USER"),
                            smtppass=settings.get("SMTP_PASS"),
                            smtpport=settings.get("SMTP_PORT"),
                            smtptls=settings.get("SMTP_TLS"),
                            smtpssl=settings.get("SMTP_SSL")
                            )
        mailer.send(to=settings.get("MAIL_RECEIVERS"),
                    subject="Booking Scrapy parser. Error report for " + datetime.today().strftime("%d.%m.%Y %H:%M"),
                    body=body,
                    )