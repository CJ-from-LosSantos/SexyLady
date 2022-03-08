import httpx
from httpx import HTTPStatusError
from loguru import logger
from lxml import etree
from pywchat import Sender

ML = logger


def make_logfile(file_name, rotation="1 week", retention="10 days"):
    """
    简单的初始化log的文件
    使用帮助: https://pythondict.com/life-intelligent/tools/loguru/
    """
    return ML.add("%s_.log" % file_name, rotation=rotation, retention=retention)


def raise_on_4xx_5xx(response):
    """
    您还可以使用这些挂钩来安装响应处理代码，例如此示例，它创建一个始终在 4xx 和 5xx 响应时引发的客户端实例。引发一个 httpx.HTTPStatusError
    """
    try:
        response.raise_for_status()
    except HTTPStatusError as e:
        ML.warning('MyError: %s & status_code== %d' % (e, response.status_code))


class SexyRequest:

    def __init__(self):
        self.SPIDER_NAME = None
        self.URLS = None
        self.METHOD = 'get'
        self.HEADERS = None
        self.RESPONSE = None
        self.client = None

    def __init_response(self, url, mode='text', **kwargs):
        """
            with httpx.Client(event_hooks={'response': [raise_on_4xx_5xx]}) as client:
                self.RESPONSE = client.request(self.METHOD, url, headers=self.HEADERS, **kwargs)
                self.RESPONSE.encoding = self.RESPONSE.apparent_encoding
            return getattr(self.RESPONSE, mode)
        """
        self.client = httpx.Client(event_hooks={'response': [raise_on_4xx_5xx]})
        self.RESPONSE = self.client.request(self.METHOD, url, headers=self.HEADERS, **kwargs)
        self.RESPONSE.encoding = self.RESPONSE.apparent_encoding
        return getattr(self.RESPONSE, mode)

    def _init_parser(self):
        for url in self.start_request():
            parser = etree.HTML(self.__init_response(url))
            yield parser.xpath

    def start_request(self):
        yield from self.URLS

    def private_response(self, mode, **kwargs):
        for url in self.start_request():
            yield self.__init_response(url, mode=mode, **kwargs)


class SexyParser:

    def __init__(self):
        self.xpath = None

    def exec_xpath(self, response):
        parser = etree.HTML(response)
        return parser.xpath

    def inn(self, source, xpath: classmethod = None, _raise=False):
        """
        用例编写:
            parser = SexyParser()
            result['hot_search'] = parser.inn('//*[@class="title-content-title"]/text()', self.xpath, _raise=True)

        :param source: xpath 语句
        :param xpath: method
        :param _raise: 异常开关
        :return:
        """
        if _raise and not xpath(source):
            raise ValueError('执行xpath(%s)为空' % source)
        elif not _raise and not xpath(source):
            ML.warning('xpath语句可能有问题: < source: %s > = None ' % source)
        else:
            return xpath(source)


class MiniWeChatBot:
    """
    用例编写:
        token = (corpid, corpsecret, agentid)
        app = MiniWeChatBot(TOKEN)
        app.wcs_text("is test message...")
        ...
    """

    def __init__(self, token):
        """
        你可以声明一个变量，该变量为：tuple，元组中包含corpid, corpsecret, agentid
        """
        self.app = Sender(*token)

    def wcs_text(self, message):
        """
        :param message: Text content sent
        """
        self.app.send_text(message)

    def wcs_image(self, path):
        """
        :param path: Sent picture address
        """
        self.app.send_image(path)

    def wcs_file(self, path):
        """
        :param path: File address sent
        """
        self.app.send_file(path)
