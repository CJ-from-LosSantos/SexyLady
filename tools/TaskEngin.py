import asyncio
import jmespath as jmp
from ruamel import yaml
from pymongo import MongoClient
from tmpl import set_spiders
from tools.LogGenerator import ML
from collections import namedtuple
from tools.RequestTool import RequestTool

TaskStatus = namedtuple('TaskStatus', 'no_start, finish, err')
TASK_STATUS = TaskStatus(0, 1, 2)


def upload_task(paths: list = None):
    """

    :param paths:
    :return:
    """
    fields = []
    classes = []  # 爬虫模板列表(类名)

    for path in paths:
        with open(path, 'r', encoding='utf-8') as doc:
            content = yaml.load(doc, Loader=yaml.Loader)
            content['status'] = 0

            user = jmp.search('database.user', content)
            pwd = jmp.search('database.password', content)
            ip = jmp.search('database.ip', content)
            port = jmp.search('database.port', content)
            dataName = jmp.search('database.DatabaseName', content)
            tableName = jmp.search('database.TableName', content)

            if not (not user or not pwd):
                _CLIENT = f'mongodb://{user}:{pwd}@{ip}:{port}'
            elif not (not (not user) or not (not pwd)):
                _CLIENT = f'mongodb://{ip}:{port}'

        fields.append(content)

        try:
            if exec_client_action(dataName, tableName, 'insert_many', fields, _CLIENT):
                ML.debug('Task list insertion complete')
        except UnboundLocalError:
            ML.warning('Check you mongo user and password')


async def start_task(DATABASE, TABLE):
    result = exec_client_action(
        DATABASE, TABLE,
        "find", (
            {}, {"_id": 0, "database": 0}
        )
    )
    # _name, _url, _async, _type = [], [], [], []
    for task in result:
        if task['status'] == TASK_STATUS.no_start:
            _name = task['name']
            _url = task['url']
            _async = task['async']

            _class = getattr(set_spiders, _name)(_name, _url, _async)
            obj = RequestTool(_class.set_spider, data=task)

            res = await obj.async_call()
            ML.info('Temporary display data: %s' % res)


def get_task():
    pass


def async_run_loop(tasks):
    """
    可以简单的调用该方法就可以启动异步的程序
    :param tasks: 任务列表
    :return: 返回任务结果
    """
    loop = asyncio.get_event_loop()
    end_tasks = asyncio.gather(*tasks)
    return loop.run_until_complete(end_tasks)


def exec_client_action(DATA, TABLE, ACTION, VALUES=None, CLIENT='mongodb://localhost:27017/'):
    client = MongoClient(CLIENT)
    try:
        db = getattr(client, DATA)
        cars = getattr(db, TABLE)
        if VALUES:
            if not isinstance(VALUES, tuple):
                return getattr(cars, ACTION)(VALUES)
            return getattr(cars, ACTION)(*VALUES)
        return getattr(cars, ACTION)()
    except Exception:
        ML.exception('err')
        return False
