"""Utilities."""

import logging

import requests
from requests.exceptions import HTTPError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

log = logger = logging


def request(method: str,
            url: str,
            max_retry: int = 2,
            params=None,
            data=None,
            json=None,
            headers=None,
            **kwargs):
    for i in range(max_retry + 1):
        try:
            response = requests.Session().request(
                method,
                url,
                params=params,
                data=data,
                json=json,
                headers=headers,
                **kwargs)
        except HTTPError as e:
            log.error(f'HTTP error:\n{e}')
            log.error(f'The No.{i + 1} request failed, retrying...')
        except KeyError as e:
            log.error(f'Wrong response:\n{e}')
            log.error(f'The No.{i + 1} request failed, retrying...')
        except Exception as e:
            log.error(f'Unknown error:\n{e}')
            log.error(f'The No.{i + 1} request failed, retrying...')
        else:
            return response

    raise Exception(f'All {max_retry + 1} HTTP requests failed, die.')


def get_cookies(cookies: str = None):
    if '#' in cookies:
        return cookies.split('#')
    else:
        return cookies.splitlines()


MESSAGE_TEMPLATE = '''
    {today:#^18}
    🔅[{region_name}]{uid}
    今日奖励: {award_name} × {award_cnt}
    本月累签: {total_sign_day} 天
    签到结果: {status}
    {end:#^18}'''
