1. 克隆项目到本地后您可以在项目的终端下输入pip命令，来安装项目所需要的模块包。

   ```shell
   pip install -r requirements.txt
   ```

2. 在准备就绪是，您的项目目录结构应该是：

   ![](https://i.bmp.ovh/imgs/2022/03/21076566c707b82a.png)

   此时，您需要运行 tools 目录下 make_template.py 文件，终端命令如下：

   ```shell
   cd .\tools\
   python .\make_template.py
   ============================
   [output]：Create template successfully
   ```

   

   此时您将会看到生成了 set_spider 和 set_parser 的.py 文件，如果未出现请重新从磁盘加载目录。

3. 接下来您可以查看生成的模板文件文档，开始熟悉。

# 开始

## 创建爬虫

1. 在 set_spider 中，您需要先设置您的抓取目标（url），比如我们可以这样：

   ```python
   class SN:
   
       def __init__(self):
           """
           Want to pass a list like this: self.urls = ['links_1', 'links_2']
           your tasks are not many. You can also do this: self.urls = 'link'
           """
           self.urls = "https://pypi.org/"
   ```

   是不是很简单呢😲？是以简单的方式完成了第一步，我们只需要设置 `self.urls` 即可，爬虫就创建完成了是😋

## 拿到数据

1. 在 set_parser 中，您只需要专注您的采集数据工作即可，选用您喜欢的解析库，我们这里帮您封装了 xpath 和 PyQuery 。比如我们可以这样：

   ```python
   class Parser:
       """
       requests_html is encapsulated here. For details, you can move to:
           https://github.com/kennethreitz/requests-html;
           https://pypi.org/project/requests-html/
   
       @:param methodname: Select the parsing method you need to use
       """
       methodname = 'xpath'
   
       def parser_source(self, p):
           """
           Show your cleaning data here, like this:
               info = self.html('//*[@id="articleContentId"]/text()')
           """
           label = p('//*[@id="user-indicator"]/nav[1]/ul/li/a/text()')
           print(label)
   ```

   在这里我们设置了 `methodname = "xpath"`，它是为了告诉 AutoCompleteParser 中，您选中了哪一款解析器，随后我们在函数 `parser_source` 使用了解析器 `p` 完成了 label 字段的采集，并且打印它。

2. 你是否已经运行程序了呢？没错，它肯定给你一个警告⚠，因为你传递错了爬虫的任务名给她，她找不到是要加载哪个爬虫文件😅，你需要更改这里：

   ```python
   if __name__ == '__main__':
       #  You can initialize your log file
       make_logfile('is_test')
   
       ML.info('Start running...')
       SexyLady.callback('SN')  # Class name corresponding to set_spider.py
   ```

   在 `SexyLady.callback('')` 中，你需要把 set_spider.py 中的类名告诉她，她才知道加载这份爬虫配置文件👌。

# 尾声

SexyLady👱‍♀️ 还在建设当中，她应该还有更多的特性，还有个更多的拓展，也希望使用者在 SexyLady 中遇到的问题❓、bug🛠，或者好的想法🎈都可以在git项目中反馈或者添加作者微信加入交流群一起讨论✈✈

git：[神经蛙/SexySpider (gitee.com)](https://gitee.com/lone_time_no_see_CJ/SpiderAPI)

WeChat：![](https://i.bmp.ovh/imgs/2022/03/36cf4bccef33fe98.jpg)

