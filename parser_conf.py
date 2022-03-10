class Parser:
    name = 'htmlxpath'

    def __init__(self, method):
        self.html = method

    def parser_source(self):
        hot = self.html.xpath('//*[@id="__next"]/div[1]/div/div/section[1]/article/h2[1]/text()')
        print(hot)
