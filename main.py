# 这是一个示例 Python 脚本。
from conf.config import TOKEN
from MiniObject import SexyRequest, SexyParser, MiniWeChatBot, ML, make_logfile


class BaiDu(SexyRequest):

    def __init__(self):
        super().__init__()
        self.xpath = None

    def set_spider(self):
        self.SPIDER_NAME = '百度爬虫'
        self.URLS = ['https://www.baidu.com/']
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
        }
        parser = self._init_parser()
        for self.xpath in parser:
            self.parser_html()

    def parser_html(self):
        result = {}
        parser = SexyParser()
        try:
            # 这是错误的例子
            result['hot_search'] = parser.inn('//*[@class="title-cont——？？？？"]/text()', self.xpath, _raise=True)
            # result['hot_search'] = parser.inn('//*[@class="title-content-title"]/text()', self.xpath, _raise=True)
        except:
            ML.exception("这里发生了什么")
        finally:
            print('result:: ', result)
            self.client.close()
            # app.wcs_file('这是测试用例_.log')


if __name__ == '__main__':
    make_logfile('这是测试用例')
    # app = MiniWeChatBot(TOKEN)
    P = BaiDu()
    P.set_spider()
