from lxml import etree
from pyquery import PyQuery as pq
from set_parser import Parser


class Auto:

    def __init__(self, g_lxml):
        self._lxml = g_lxml.text

    async def async_call(self, *args, **kwargs):
        """
        负责调用 parser_conf 对象中的 parser_source方法，执行自动数据解析
        """
        if Parser.methodname == 'xpath':
            Parser().parser_source(etree.HTML(self._lxml))
        elif Parser.methodname == 'xpath':
            Parser().parser_source(pq(self._lxml))

    def commonly_call(self, *args, **kwargs):
        """
        负责调用 parser_conf 对象中的 parser_source方法，执行自动数据解析
        """
        if Parser.methodname == 'xpath':
            Parser().parser_source(etree.HTML(self._lxml).xpath)
        elif Parser.methodname == 'pq':
            Parser().parser_source(pq(self._lxml))

