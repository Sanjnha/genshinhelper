"""Utilities."""

import hashlib
import logging
import random
import string
import time

import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

log = logger = logging


def request(method: str,
            url: str,
            max_retries: int = 2,
            params=None,
            data=None,
            json=None,
            headers=None,
            **kwargs):
    # The first HTTP(S) request is not a retry, so need to + 1
    total_requests = max_retries + 1
    for i in range(total_requests):
        try:
            response = requests.Session().request(
                method,
                url,
                params=params,
                data=data,
                json=json,
                headers=headers,
                timeout=21,
                **kwargs)
        except Exception as e:
            log.error(f'Request failed: {url}\n{e}')
            if i == max_retries:
                raise Exception(f'Request failed ({i + 1}/{total_requests}):\n{e}')

            seconds = 5
            log.info(f'Trying to reconnect in {seconds} seconds ({i + 1}/{max_retries})...')
            time.sleep(seconds)
        else:
            return response


def get_cookies(cookies: str = None):
    if '#' in cookies:
        return cookies.split('#')
    else:
        return cookies.splitlines()


def extract_cookie(name: str, cookie: str):
    if name not in cookie:
        raise Exception('Failed to extract cookie: '
            f'The cookie does not contain the `{name}` field.')
    extract_cookie = cookie.split(f'{name}=')[1].split(';')[0]
    return extract_cookie


def cookie_to_dict(cookie):
    cookie_dict = dict([l.split('=', 1) for l in cookie.split('; ')])
    return cookie_dict


def hexdigest(text):
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


def get_ds(type: str = None):
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
    return (client_type, app_version, ds)


MESSAGE_TEMPLATE = '''
    {today:#^18}
    🔅[{region_name}]{uid}
    今日奖励: {award_name} × {award_cnt}
    本月累签: {total_sign_day} 天
    签到结果: {status}
    {travel_notes}
    {end:#^18}'''
