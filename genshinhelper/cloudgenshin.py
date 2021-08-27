from .exceptions import GenshinHelperException
from .utils import request, _


class CloudGenshinCheckin(object):
    def __init__(self, headers: dict):
        self._headers = headers

    def run(self):
        url = 'https://api-cloudgame.mihoyo.com/hk4e_cg_cn/wallet/wallet/get'

        response = request('get', url, headers=self._headers).json()
        message = response.get('message')
        if response.get('retcode') != 0:
            raise GenshinHelperException(message)

        data = response.get('data', {})
        free_time = data.get('free_time', {}).get('free_time', -1)
        free_time_limit = data.get('free_time', {}).get('free_time_limit', -1)
        total_time = data.get('total_time', -1)
        result_str = _('''    签到结果: {}
        免费时长: {} / {}
        总计时长: {}
        ''').format(message,
            self.hours(free_time),
            self.hours(free_time_limit), self.hours(total_time))

        return result_str

    def hours(self, minute):
        minute = int(minute)
        if minute < 0:
            raise ValueError('Input number cannot be negative')

        hours = int(minute / 60)
        minutes = minute % 60
        result = _('{} 小时 {} 分钟').format(
            hours, minutes) if minutes != 0 else _('{} 小时').format(hours)
        return result

