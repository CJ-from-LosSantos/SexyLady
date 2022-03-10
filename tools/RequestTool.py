from httpx import HTTPStatusError
from tools.LogGenerator import ML


def raise_on_4xx_5xx(response):
    """
    您还可以使用这些挂钩来安装响应处理代码，例如此示例，它创建一个始终在 4xx 和 5xx 响应时引发的客户端实例。引发一个 httpx.HTTPStatusError
    """
    try:
        response.raise_for_status()
    except HTTPStatusError as e:
        ML.warning('MyError: %s & status_code== %d' % (e, response.status_code))


