import inspect
from lxml import etree
from httpx import HTTPStatusError
from loguru import logger


# from pyquery import PyQuery as pq


def callback():
    from tmpl import set_spiders
    clsmembers = inspect.getmembers(set_spiders, inspect.isclass)
    classes = []
    for (name, _) in clsmembers:
        classes.append(name)


class Loggings:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Loggings, cls).__new__(cls, *args, **kwargs)

        return cls.__instance

    @staticmethod
    def init_logger():
        return logger


ML = Loggings().init_logger()


class RequestTool:

    def __init__(self, response, **kwargs):
        self.response = response
        self.kwargs = kwargs.get('data', ValueError('Unknown parameter error executing task'))

    def raise_on_4xx_5xx(self):
        """
        您还可以使用这些挂钩来安装响应处理代码，例如此示例，它创建一个始终在 4xx 和 5xx 响应时引发的客户端实例。引发一个 httpx.HTTPStatusError
        """
        try:
            self.response.raise_for_status()
        except HTTPStatusError as e:
            ML.warning('MyError: %s & status_code== %d' % (e, self.response.status_code))

    async def async_call(self):

        fields = []
        if self.kwargs['type'] == 'text':

            if self.kwargs['parser'] == 'xpath':
                for resp in self.response:
                    xp_html = etree.HTML(resp.text).xpath
                    for inx, rule in enumerate(self.kwargs['rule']):
                        fields.append(
                            {
                                self.kwargs['field'][inx]: xp_html(rule)
                            }
                        )
            elif self.kwargs['parser'] == 'pyquer':
                # 目前最好是使用 xpath 解析，对 PyQuery 封装未完全
                raise ValueError('You should not choose < PyQuery > as your parser at this time')
                # for resp in self.response:
                #     pq_html = pq(resp.text)

        else:
            for resp in self.response:
                return getattr(resp, self.kwargs['type'])()

        return fields

    def exec_action_html(self, _html):
        pass


class Auto:

    def __init__(self, _html):
        self.html = _html

    def exec_action_html(self):
        pass

    async def setup(self):
        """
        目前最好是使用 xpath 解析，对 PyQuery 封装未完全
        :return:
        """
        raise ValueError('You should not choose < PyQuery > as your parser at this time')
        # self.exec_action_html()
        # print(type(self.html))
