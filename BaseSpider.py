import os
import time

import requests
from requests_cache import install_cache

from lxml import etree
from pymongo import MongoClient
from loguru import logger
from pywchat import Sender


class Spider:

    def __init__(self):
        self.SPIDER_NAME = None
        self.BASE_URL = None
        self.METHOD = 'get'
        self.HEADERS = None
        self.XPATH = None
        self.RESPONSE = None
        self.IP = None
        self.PORT = None
        self.client = None
        self.LOG = logger
        self.TOKEN = None

    def __init_response(self, hook_time, mode='text', **kwargs):
        try:
            install_cache('%s_spider_session_cache' % self.SPIDER_NAME)
            # requests_cache.clear()
            session = requests.session()
            session.hooks = {'response': self.make_throttle_hook(hook_time)}
            self.RESPONSE = session.request(self.METHOD, self.BASE_URL, headers=self.HEADERS, **kwargs)
            self.RESPONSE.raise_for_status()
        except requests.HTTPError as e:
            raise requests.HTTPError('Error: %s & status_code== %d' % (e, self.RESPONSE.status_code))
        self.RESPONSE.encoding = self.RESPONSE.apparent_encoding
        return getattr(self.RESPONSE, mode)

    def __init_mongodb(self):
        self.client = MongoClient('mongodb://{}:{}/'.format(self.IP, self.PORT))
        return self.client

    def _init_logger(self, file_name):
        return self.LOG.add("%s_.log" % file_name, rotation="1 week", retention="10 days")

    def _init_parser(self, hook_time=2):
        parser = etree.HTML(self.__init_response(hook_time))
        self.XPATH = parser.xpath

    def wcs_text(self, message):
        app = Sender(self.TOKEN)
        app.send_text(message)

    def wcs_image(self, path):
        app = Sender(self.TOKEN)
        app.send_image(path)

    def wcs_file(self, path):
        app = Sender(self.TOKEN)
        app.send_file(path)

    def insert_many(self, cars, database='test', cars_name='test'):
        _ = self.__init_mongodb()
        with self.client:
            db = self.client[database]
            db[cars_name].insert_many(cars)

    def item_filter(self, key: str, values: list, pp: list):
        res = []
        for value in values:
            if value in pp:
                break
            res.append({key: value})
        return res

    def private_response(self, mode, **kwargs):
        return self.__init_response(mode=mode, **kwargs)

    # def private_mongodb(self):
    #     return self.__init_mongodb()

    @staticmethod
    def make_throttle_hook(timeout=0.1):
        def hook(response, *args, **kwargs):
            if not getattr(response, 'from_cache', False):
                print(f'Not cache, So Wait {timeout} second...')
                time.sleep(timeout)
            return response

        return hook

    @staticmethod
    def exit():
        os._exit(1)
