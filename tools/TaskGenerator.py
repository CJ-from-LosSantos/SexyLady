import asyncio
from tools.LogGenerator import ML


def generate_async_task(async_function, urls: list) -> list:
    try:
        return [asyncio.ensure_future(async_function(url)) for url in urls]
    except:
        ML.exception('ERROR Snapshot')
    finally:
        ML.info('Creation Task is Completed, have %d task' % len(urls))


def generate_task(_function, urls: list) -> list:
    try:
        return [_function(url) for url in urls]
    except:
        ML.exception('ERROR Snapshot')
    finally:
        ML.info('Creation Task is Completed, have %d task' % len(urls))


def async_run_loop(tasks):
    loop = asyncio.get_event_loop()
    end_tasks = asyncio.gather(*tasks)
    return loop.run_until_complete(end_tasks)
