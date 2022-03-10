from requests_html import HTML
from parser_conf import Parser


class Auto:

    def __init__(self, response):
        self.response = response.text

    async def __call__(self, *args, **kwargs):
        """
        负责调用 parser_conf 对象中的 parser_source方法，执行自动数据解析
        """
        doc = getattr(HTML(html=self.response), Parser.methodname)
        Parser(doc).parser_source()
