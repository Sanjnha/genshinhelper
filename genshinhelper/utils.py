"""Utilities."""

import hashlib
import logging
import random
import string
import time

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


def hexdigest(text):
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


def get_ds(type: str=None):
    # 1:  ios
    # 2:  android
    # 4:  pc web
    # 5:  mobile web
    if not type or type == '5' or type == 'mobileweb':
        client_type = '5'
        app_version = '2.3.0'
        salt = 'h8w582wxwgqvahcdkpvdhbh2w9casgfl'
    elif type == '2' or type == 'android':
        client_type = '2'
        app_version = '2.8.0'
        salt = 'dmq2p7ka6nsu0d3ev6nex4k1ndzrnfiy'
    i = str(int(time.time()))
    r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
    c = hexdigest(f'salt={salt}&t={i}&r={r}')
    ds = f'{i},{r},{c}'
    return client_type, app_version, ds


MESSAGE_TEMPLATE = '''
    {today:#^18}
    🔅[{region_name}]{uid}
    今日奖励: {award_name} × {award_cnt}
    本月累签: {total_sign_day} 天
    签到结果: {status}
    {end:#^18}'''

