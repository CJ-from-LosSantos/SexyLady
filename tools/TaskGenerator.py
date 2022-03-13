import asyncio
import inspect
from conf.config import REDIS
from tools.LogGenerator import ML
from redis import StrictRedis


def upload_task(tmplName=None, taskUrl=None):
    """
    负责上传 url 和对应爬虫模板的 ”set_spider.py中的类名“ 到 redis 中
    :param tmplName: 对应爬虫模板的类名，用户如果没有传递则获取所有爬虫模板下的所有类名
    :param taskUrl: 任务url
    :return:
    """

    _redis = StrictRedis(*REDIS)
    pl = _redis.pipeline()

    if tmplName:
        ok = _redis.hsetnx('Task_table', tmplName, taskUrl)
        if not ok:
            ML.debug('Task exists')
        else:
            ML.debug('Task: %s insertion complete' % {'Field': tmplName, 'Value': taskUrl})
        return 1

    classes = []  # 爬虫模板列表(类名)
    success = []  # 添加任务成功列表,用于日志显示
    fail = []  # 添加任务失败列表,用于日志显示

    from tmpl import set_spiders
    clsmembers = inspect.getmembers(set_spiders, inspect.isclass)
    for (name, _) in clsmembers:
        """
        Only：
            one spider tmpl --> one set_parser file
            one spider tmpl --> many set_parser file
        """
        pl.hsetnx('Task_table', name, taskUrl)
        classes.append(name)
    end_execute = pl.execute()

    for inx, YN in enumerate(end_execute):
        if YN:
            success.append(classes[inx])
        else:
            fail.append(classes[inx])
    ML.debug('Task list: %s insertion complete' % {'Field': success})
    ML.debug('Task list: %s exists' % {'Field': fail})

    return 1


def generate_async_task(async_function, urls: list) -> list:
    try:
        return [asyncio.ensure_future(async_function(url)) for url in urls]
    except:
        ML.exception('ERROR Snapshot')
    finally:
        ML.debug('Creation Task is Completed, have %d task' % len(urls))


def generate_task(_function, urls: list) -> list:
    try:
        return [_function(url) for url in urls]
    except:
        ML.exception('ERROR Snapshot')
    finally:
        ML.debug('Creation Task is Completed, have %d task' % len(urls))


def async_run_loop(tasks):
    """
    可以简单的调用该方法就可以启动异步的程序
    :param tasks: 任务列表
    :return: 返回任务结果
    """
    loop = asyncio.get_event_loop()
    end_tasks = asyncio.gather(*tasks)
    return loop.run_until_complete(end_tasks)
