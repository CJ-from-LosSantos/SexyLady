# SexyLady version 0.5

## 前言：

​		首先距离SexyLady上个版本发布已经过去八天了，SexyLady的出世是因为那段时间处于休息阶段，而正好在发布v.01后的两天里，我由之前的银行跳到了新的科技公司。而这个阶段我更多的是投入到工作当中，帮公司设计自动化的架构，所以SexyLady这段时间并未更新，但我发誓，我无时无刻在想着她，如名字一样让人痴迷😍

SexyLady的逻辑是让用户更专注如何取得数据而不是怎样写爬虫，旨在降低编写爬虫的门槛。SexyLady更适合在组织中使用，或者大规模采集上更能体现这位女郎的优势。用户只需要对一个爬虫任务建造一个task.yaml文件及对应一个爬虫任务，而set_spiders里面拥有您设置后的所有爬虫模板，爬虫它不用在想写数学公式一样先写解：再来因为所以，科学道理了。而模板也不需要经常的改变，某些关键的参数算法或者规则也如数学公式一样可复用套用，最后都指向一个结果。所以这就是SexyLady的核心。

​		对于SexyLady新版的介绍我会在下面开展，我也希望能有拥有更多的观众和热爱技术的人一起加到SexyLady这个大家庭，也非常希望大家由上能够认真的看到结尾的🤗

## 准备工作

1. 克隆项目到本地后您可以在项目的终端下输入pip命令，来安装项目所需要的模块包。如果失败可以尝试使用国内镜像源

   ```shell
   pip install -r requirements.txt
   ```

2. 在准备就绪时，您的项目目录结构应该是：

   ![](https://i.bmp.ovh/imgs/2022/03/acd5c7d4cd7b0e53.png)

   此时您需要自己创建一个名为 `tmpl` 的目录，然后运行 tools 目录下 make_template.py 文件，如果是终端命令结果应是这样：

   ```shell
   cd .\tools\
   python .\make_template.py
   ============================
   output：Create template successfully
   ```

   

   此时您将会看到生成了 set_spiders.py 和 first_job.ymal 的两份文件，如果未出现请重新从磁盘加载目录，接下来您可以查看生成的模板文件文档，开始熟悉。

   ![](https://i.bmp.ovh/imgs/2022/03/95389141753d516c.png)

3. SexyLady是建立在 `redis` 和 `mongodb` 上的，所以你可以现在自己电脑上下载 `mongodb` ，教程链接如下：

   https://blog.csdn.net/weixin_41466575/article/details/105326230

## 开始

### 理解SexyLady爬虫

如果上面的准备步骤您都结束了，特别是 `mongodb` 那么我们接下来就可以构造爬虫了是😋

我认为的爬虫只有两步：

1. 分析网址再构造爬虫并得到正确的响应体
2. 拿到你需要的数据

SexyLady的核心，或者说未来的逻辑不会再去更改了，只会增加新的特性和维护，这里我会具体在结尾说明。那么我们先关注核心部位那就是拿到数据。SexyLady应该是让您专注如何取得数据，所以您可以直接编辑 `.yaml` 文件，yaml文件就是您这个爬虫的核心，没有yaml文件你的爬虫不会去运行，首先我们拿 requests帮助文档的网址来进行测试 `https://docs.python-requests.org/zh_CN/latest/user/quickstart.html`：

## 编辑任务yaml文件

```yaml
name: RequestsDoc
url: https://docs.python-requests.org/zh_CN/latest/user/quickstart.html
async: False
type: text
parser: xpath
database:
  user:
  password:
  ip: localhost
  port: 27017
  DatabaseName: job
  TableName: task_table
insert:
  user:
  password:
  ip: localhost
  port: 27017
  DatabaseName: data
  TableName: info_table
field:
  - title
rule:
  - //*[@id="module-requests.models"]/p[1]/text()[1]
```

复制这段`yaml`文件内容替换生成好的`yaml`文件，随后在`tmpl`文件夹中新建一份 `main.py` 文件，它将做为启动爬虫的入口，是不很激动🤤

## 编辑入口文件

```python
# main.py
import asyncio

from Base.TaskEngin import start_task


async def main(command, *args):
    if command == 'start':
        await start_task('job', 'task_table')


if __name__ == '__main__':
    asyncio.run(main('start'))
```

就这么点内容，我的爬虫及设置好了？真是老母牛踩电线，牛🍺带闪电...了😮

SexyLady不伦是任务还是爬虫都是建立在异步上的，我想这样SexyLady的逻辑在业务场景上处理让任务更加通顺，所以更适合组织架构去使用它。如果您运行后存在模块包问题，可以尝试在第一个导包上面加上 `sys.path.append(os.getcwd())` ，那么接下来请运行它，你会看到你的终端上什么都没有并且程序运行结束了，可是我刚刚的确说了只需要一份yaml文件他就可以启动了😵。在这里我就要告诉你为什么准备工作哪里需要安装`redis`和`mongodb`了，SexyLady会从您配置好的yaml文件中把任务上传到mongo中，随后爬虫会在mongo中读取任务再去执行它，所以这是它的逻辑。你并不能直接对他start，而是需要先create。我们把文件该写如下：

```python
import asyncio
from Base.TaskEngin import upload_task, start_task


async def main(command, *args):
    if command == 'create':
        print('执行上传任务')
        upload_task(['first_job.yaml'])
    elif command == 'start':
        print('执行任务')
        await start_task('job', 'task_table')


if __name__ == '__main__':
    asyncio.run(main('create'))
    
# output：Task list insertion complete
```

这时如果您的mongo没有问题，可以正常连接，可以看到有一个`job`数据库，数据库下有一个集合叫做`task_table`，没错，这正是您在yaml文件中设置好的database字段下的内容。

![](https://i.bmp.ovh/imgs/2022/03/c1bf2fa7f457a550.png)

在该集合中存储的信息你都可以在您编辑好的yaml文件中找到，刚刚创建完任务后，接下来我们再执行任务，`asyncio.run(main('start'))`，把`create`改写成`start`。此时您会看到 `Check whether you have configured the spider template: RequestsDoc`，这是后您应该去看看您的爬虫模板中是否有`RequestsDoc`这个类是😭，相信我，这不是再折磨你，而是更好的告诉你如何上手这款框架，因为作者本人也经常cv大法而忘记这个地方😂

重新运行，你会看到三条亮眼的日志，并且友好的临时告知了你取到的数据结果

![](https://i.bmp.ovh/imgs/2022/03/2337a4ed5e0f729c.png)

## 打造div王国

我相信上面的一个简单的例子应该能够让您上手这款框架，最起码简单的操作是会的。接下来我们一起理解下SexyLady中的yaml的🧐

### yaml

```yaml
name: RequestsDoc
url: https://docs.python-requests.org/zh_CN/latest/user/quickstart.html
async: False
type: text
parser: xpath
database:
  user:
  password:
  ip: localhost
  port: 27017
  DatabaseName: job
  TableName: task_table
insert:
  user:
  password:
  ip: localhost
  port: 27017
  DatabaseName: data
  TableName: info_table
field:
  - title
rule:
  - //*[@id="module-requests.models"]/p[1]/text()[1]
```

​		在这里你可能需要了解一些简单yaml文件的知识，那么在SexyLady中每一份yaml文件里的`name`都是对应您的`set_spiders`里爬虫模板，当然您也可以理解成是一个对象或者类，我更倾向叫它模板。`url`则是你需要抓取的目标，`asyns`看起来是不是很熟悉，并且在set_spiders中每个模板都会在需要一个`_async`，它就是你自己设置这个爬虫任务是否考虑异步爬取，一个简单的开关。随后`type`和`parser`都是较为重要的，`type`对应网址的数据是什么格式，这里我们选用`text`是应为数据可以从`html`中拿到，它并不是一个需要从`json`里或者`api`返回出来的数据。而parser就是你选取的解析方法，在这块我封装了xpath和PyQuery，当然为了保险起见，目前这个版本不开放PyQuery的解析器。

​		接下来就是数据库方面。在`database`中，可以很清晰的看到你的任务放在那个数据库中，您只需要自己更改对应的字段即可，不论您是在公司去使用它还是个人使用。`insert`则是你的采集的数据回存在mongo中或者其他数据库中，当然，目前这个版本并没有把它公布出来，正和PyQuery一样，它可能存在不稳定性，我也很希望有更多使用它的观众能够及时在交流群反馈或者提交lssuse。

`field`它对应着您的的`rule`，您可以把它理解成一个字典，`field`里存放的都是键，而`rule`则是值。

### set_spider

```python
from Base import SexyLady
from tools.LogGenerator import *


class Spider1:

    def __init__(self, name, urls, _async):
        if self.__class__.__name__ != name:
            raise ValueError('WTF is different')
        self.urls = urls
        self._async = _async

    @property
    def set_spider(self):
        """
        在这里掌控你的蜘蛛，告诉它如何得到正确的响应
        如果你想使用微信机器人，您可以先查看conf文件夹里的图片
        Take control of your spider here and tell it how to get the right response
        You can get the activated app, which can automatically send some customized messages or files to your wechat
        Please check the picture under the conf file for details
        """
        # app = SexyLady.MiniWeChatBot(TOKEN)
        ML.debug('Calling %s %s file' % (__file__.split('\\')[-1], self.__class__.__name__))
        try:
            return iter(SexyLady.Request(urls=self.urls, is_async=self._async).builder)
        except:
            ML.exception('ERROR Snapshot')
        finally:
            pass
            # app.wcs_file('is_test_.log')
```

​		set_spiders中要讲的其实没有很多，因为强调过很多次SexyLady的特性就是让您专注在数据解析，而不是一直写解求证答案，所以我想她能有出色的发挥，至少在某一方面的🤔。你需要传递一些请求体需要用到的参数，或者是一些代码得到的结果，并把它丢到请求中。同时在还未公开的版本中对于set_spiders其实有一块较大的改变，我相信很也快就能和大家见面👨‍💻。

​		SexyLady也需要您更多的探索和反馈，她才能更加让人着迷是🎗🎗

## 尾声

### 为什么SexyLady的核心，或者说未来的逻辑不会再去更改了，只会增加新的特性和维护？

​		SexyLady第一个版本是v0.1，第二个发行版是v0.5。短短一周而已，就能把SexyLady框架的逻辑设计直接颠覆性重写，之前是编写set_parser.py现在直接变成yaml文件，中间很多的逻辑都是直接删文件重写，所以在脑海中推翻了许多核心逻辑的设计，就如联盟中死在狼人手里的海牛阿福一般。一个人做一个框架很累的，不是简单写几个文件就能说是框架，要考虑到很多兼容性问题以及未来的产品规划。而在这一段时间对这个框架的开发只有默默的一个人，甚至一些不太友好的评价。我个人是很喜欢造轮子，从我写第一个hello word的时候我就偏不写它，写老八·奥里给

​		所以我希望能在此平台得到更多观众吸纳更多优秀的开发人员一起改良这个还不是很性感的女郎，真挚的欢迎大家加入！记得给小星星哦~⭐
