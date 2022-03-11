import httpx
import set_spider
from faker import Factory
from pywchat import Sender
from tools.LogGenerator import ML
from tools.AutoCompleteParser import Auto
from tools.TaskGenerator import generate_async_task, generate_task


def callback(set_spider_name):
    try:
        NAME = set_spider_name
        getattr(set_spider, NAME)().set_spider()
    except AttributeError:
        ML.warning('Bad task name: < %s >' % set_spider_name)


class AsyncClient:
    """
    返回异步客户端
    """

    def __call__(self, *args, **kwargs):
        return httpx.AsyncClient(**kwargs)


class Client:
    """
    返回普通客户端
    """

    def __call__(self, *args, **kwargs):
        return httpx.Client(**kwargs)


class Request:

    def __init__(
            self, urls=None, methode='get', is_async=False,
            content=None, data=None, files=None, json=None,
            params=None, headers=None, cookies=None, auth=None,
            follow_redirects=None, timeout=None, extensions=None, **kwargs
    ):
        self.urls = urls
        self.methode = methode
        self.is_async = is_async
        self.client = AsyncClient().__call__(**kwargs) if is_async else Client().__call__(**kwargs)
        self.result = [self.methode, self.urls]

        self.content = content
        self.data = data
        self.files = files
        self.json = json
        self.params = params
        self.headers = headers or {'User-Agent': Factory.create().user_agent()}
        self.cookies = cookies
        self.auth = auth
        self.follow_redirects = follow_redirects
        self.timeout = timeout
        self.extensions = extensions

    async def async_out_response(self, url):
        response = await self.client.request(
            method=self.methode, url=url,
            content=self.content, data=self.data,
            json=self.json, params=self.params,
            headers=self.headers, cookies=self.cookies,
            auth=self.auth, follow_redirects=self.follow_redirects,
            timeout=self.timeout, extensions=self.extensions,
        )
        await Auto(response).async_call()
        ML.info('End of request %s, %s, FROM %s' % (url, response, self.client))
        return response

    def out_response(self, url):
        try:
            response = self.client.request(
                method=self.methode, url=url,
                content=self.content, data=self.data,
                json=self.json, params=self.params,
                headers=self.headers, cookies=self.cookies,
                auth=self.auth, follow_redirects=self.follow_redirects,
                timeout=self.timeout, extensions=self.extensions,
            )
            Auto(response).commonly_call()
            ML.info('End of request %s, %s, FROM %s' % (self.urls, response, self.client))
            return response
        except Exception as e:
            print(e)
        finally:
            self.client.close()

    def builder(self):
        """
        解析 urls列表 并且传入到请求中 \
        是列表+是异步；是列表+不是异步；不是列表+是异步；不是列表+不是异步
        :return: 异步模式下返回任务列表，单例下是 response
        """
        if isinstance(self.urls, list) and self.is_async:
            return generate_async_task(self.async_out_response, self.urls)
        elif isinstance(self.urls, list) and not self.is_async:
            return generate_task(self.out_response, self.urls)
        elif isinstance(self.urls, str) and self.is_async:
            return generate_async_task(self.async_out_response, [self.urls])
        elif isinstance(self.urls, str) and not self.is_async:
            return generate_task(self.out_response, [self.urls])
        else:
            pass

#
# class SexyParser:
#
#     def __init__(self):
#         self.xpath = None
#
#     def exec_xpath(self, response):
#         parser = etree.HTML(response)
#         return parser.xpath
#
#     def inn(self, source, xpath: classmethod = None, _raise=False):
#         """
#         用例编写:
#             parser = SexyParser()
#             result['hot_search'] = parser.inn('//*[@class="title-content-title"]/text()', self.xpath, _raise=True)
#
#         :param source: xpath 语句
#         :param xpath: html
#         :param _raise: 异常开关
#         :return:
#         """
#         if _raise and not xpath(source):
#             raise ValueError('执行xpath(%s)为空' % source)
#         elif not _raise and not xpath(source):
#             ML.warning('xpath语句可能有问题: < source: %s > = None ' % source)
#         else:
#             return xpath(source)


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
