import os

import requests
from lxml import etree
from pymongo import MongoClient
from loguru import logger


class Spider:

    def __init__(self):
        self.BASE_URL = None
        self.METHOD = 'get'
        self.HEADERS = None
        self.XPATH = None
        self.RESPONSE = None
        self.IP = None
        self.PORT = None
        self.client = None
        self.LOG = logger

    def __init_response(self, mode='text', **kwargs):
        try:
            self.RESPONSE = requests.request(self.METHOD, self.BASE_URL, headers=self.HEADERS, **kwargs)
            self.RESPONSE.raise_for_status()
        except requests.HTTPError as e:
            raise requests.HTTPError('Error: %s & status_code== %d' % (e, self.RESPONSE.status_code))
        self.RESPONSE.encoding = self.RESPONSE.apparent_encoding
        return getattr(self.RESPONSE, mode)

    def __init_mongodb(self):
        self.client = MongoClient('mongodb://{}:{}/'.format(self.IP, self.PORT))
        return self.client

    def __init_logger(self, fileName):
        return self.LOG.add("%s_.log" % fileName, rotation="1 week", retention="10 days")

    def _init_parser(self):
        parser = etree.HTML(self.__init_response())
        self.XPATH = parser.xpath

    def insert_many(self, cars, database='test', carsName='test'):
        _ = self.__init_mongodb()
        with self.client:
            db = self.client[database]
            db[carsName].insert_many(cars)

    def item_filter(self, key: str, values: list, pp: list):
        res = []
        for value in values:
            if value in pp:
                break
            res.append({key: value})
        return res

    # def private_mongodb(self):
    #     return self.__init_mongodb()

    def private_response(self, mode, **kwargs):
        return self.__init_response(mode=mode, **kwargs)

    @staticmethod
    def exit():
        os._exit(1)
