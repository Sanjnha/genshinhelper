from .exceptions import GenshinHelperException
from .utils import request


def get_ledger(cookie, bind_uid, bind_region, month=0):
    url = 'https://hk4e-api.mihoyo.com/event/ys_ledger/monthInfo'
    payload = {
        'month': month,
        'bind_uid': bind_uid,
        'bind_region': bind_region,
        'bbs_presentation_style': 'fullscreen',
        'bbs_auth_required': True,
        'mys_source': 'GameRecord'
    }
    headers = {
        'Referer': 'https://webstatic.mihoyo.com/ys/event/e20200709ysjournal/index.html?bbs_presentation_style=fullscreen&bbs_auth_required=true&mys_source=GameRecord',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.8.0',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': cookie
    }
    response = request('get', url, headers=headers, params=payload).json()
    if response.get('retcode') != 0:
        return {
            'month': response.get('message'),
            'day_primogems': -1,
            'day_mora': -1,
            'month_primogems': -1,
            'month_mora': -1
        }

    day_data = response.get('data', {}).get('day_data', {})
    month_data = response.get('data', {}).get('month_data', {})
    month = response.get('data', {}).get('data_month', -1)
    day_primogems = day_data.get('current_primogems', -1)
    day_mora = day_data.get('current_mora', -1)
    month_primogems = month_data.get('current_primogems', -1)
    month_mora = month_data.get('current_mora', -1)
    ledger = {
        'month': month,
        'day_primogems': day_primogems,
        'day_mora': day_mora,
        'month_primogems': month_primogems,
        'month_mora': month_mora
    }
    return ledger

