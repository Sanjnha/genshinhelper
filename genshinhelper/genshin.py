"""genshinhelper.
Automatically get Genshin Impact daily check-in rewards from miHoYo bbs and HoYoLAB Community.

GitHub:
    https://github.com/y1ndan/genshinhelper
"""
import json
import time
import uuid
from functools import wraps

from . import journal
from .config import config
from .exceptions import CookiesExpired
from .utils import MESSAGE_TEMPLATE, log, request, get_ds


def _data_handler(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if 'Yuanshen' in self.__class__.__name__:
            self.get_roles()
            roles = self.ROLES_INFO
            if roles and (roles.get('retcode', 1) != 0 or not roles.get('data')):
                raise CookiesExpired(roles.get('message', 'Empty roles data'))
            role_list = roles.get('data', {}).get('list', [])
            if roles and not role_list:
                raise Exception(roles.get('message', 'Empty roles list'))
            if role_list:
                result_list = []
                log.info(f'当前账号绑定了 {len(role_list)} 个角色')
                for role in role_list:
                    # cn_gf01:  天空岛
                    # cn_qd01:  世界树
                    region = role.get('region', 'cn')
                    region_name = role.get('region_name', 'CN')
                    uid = role.get('game_uid', 123456789)
                    self.INFO_URL = self._INFO_URL.format(region, self.ACT_ID, uid)
                    post_data = {
                        'act_id': self.ACT_ID,
                        'region': region,
                        'uid': uid
                    }
                    self._sign_data.update({
                        'region': region,
                        'region_name': region_name,
                        'uid': uid,
                        'post_data': post_data
                    })
                    result_list.append(func(self, *args, **kwargs))
                return ''.join(result_list)
        elif 'Genshin' in self.__class__.__name__:
            try:
                self._sign_data['uid'] = self._cookie.split('account_id=')[
                    1].split(';')[0]
            except Exception as e:
                raise Exception(e)
            self._sign_data['post_data'] = {'act_id': self.ACT_ID}
            return func(self, *args, **kwargs)

    return wrapper


class __BaseCheckin(object):
    USER_AGENT = ''
    REFERER_URL = ''
    ROLES_INFO = ''
    INFO_URL = ''
    REWARD_URL = ''
    SIGN_URL = ''

    def __init__(self, cookie: str = None):
        self._cookie = cookie
        self._sign_data = {}

    def get_header(self):
        header = {
            'Cookie': self._cookie,
            'User-Agent': self.USER_AGENT,
            'Referer': self.REFERER_URL,
            'Accept-Encoding': 'gzip, deflate, br'
        }
        return header

    @property
    def _sign_info(self):
        try:
            response = request(
                'get', self.INFO_URL, headers=self.get_header()).json()
        except Exception as e:
            raise Exception(e)
        return response

    @property
    def _rewards_info(self):
        try:
            response = request(
                'get', self.REWARD_URL, headers=self.get_header()).json()
        except Exception as e:
            raise Exception(e)
        return response

    @_data_handler
    def run(self):
        sign_info = self._sign_info
        rewards_info = self._rewards_info

        today = sign_info.get('data', {}).get('today', '1970-01-01')
        total_sign_day = sign_info.get('data', {}).get(
            'total_sign_day', 0)
        is_sign = sign_info.get('data', {}).get('is_sign')
        first_bind = sign_info.get('data', {}).get('first_bind')
        awards = rewards_info.get('data', {}).get('awards', [])
        region_name = self._sign_data.get('region_name', 'Global')
        uid = self._sign_data.get('uid', 123456789)
        hidden_uid = str(uid).replace(str(uid)[3:-3], '***', 1)
        data = self._sign_data.get('post_data', {})
        region = self._sign_data.get('region')
        travel_notes = 'Olah! Odomu'
        if region in ['cn_gf01', 'cn_qd01']:
            ledger = journal.get_ledger(self._cookie, uid, region)
            travel_notes = '''旅行者 {month} 月札记
    💠原石: {month_primogems}
    🌕摩拉: {month_mora}'''.format(**ledger)

        message = {
            'today': today,
            'region_name': region_name,
            'uid': hidden_uid,
            'total_sign_day': total_sign_day,
            'travel_notes': travel_notes,
            'end': ''
        }

        log.info(f'准备为旅行者 {hidden_uid} 签到...')
        time.sleep(5)

        if is_sign:
            message['award_name'] = awards[total_sign_day - 1].get('name')
            message['award_cnt'] = awards[total_sign_day - 1].get('cnt')
            message['status'] = '👀 旅行者, 你已经签到过了哦'

            # return ''.join(self.message.format(**message))
            return self.message.format(**message)
        else:
            message['award_name'] = awards[total_sign_day].get('name')
            message['award_cnt'] = awards[total_sign_day].get('cnt')
        if first_bind:
            message['status'] = '💪 旅行者, 请先手动签到一次'

            return self.message.format(**message)

        try:
            response = request('post', self.SIGN_URL, headers=self.get_header(
            ), data=json.dumps(data, ensure_ascii=False)).json()
        except Exception as e:
            raise Exception(e)
        # 0:      success
        # -5003:  already checked in
        code = response.get('retcode', 99999)
        if code != 0:
            return response
        message['total_sign_day'] = total_sign_day + 1
        message['status'] = response.get('message')

        log.info('签到完毕')
        return self.message.format(**message)

    @property
    def message(self):
        return MESSAGE_TEMPLATE


class YuanshenCheckin(__BaseCheckin):
    ACT_ID = 'e202009291139501'
    USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/{}'
    REFERER_URL = 'https://webstatic.mihoyo.com/bbs/event/signin-ys/index.html?bbs_auth_required={}&act_id={}&utm_source={}&utm_medium={}&utm_campaign={}'.format('true', ACT_ID, 'bbs', 'mys', 'icon')
    ROLES_INFO = {}
    INFO_URL = ''
    ROLE_URL = 'https://api-takumi.mihoyo.com/binding/api/getUserGameRolesByCookie?game_biz={}'.format('hk4e_cn')
    _INFO_URL = 'https://api-takumi.mihoyo.com/event/bbs_sign_reward/info?region={}&act_id={}&uid={}'
    REWARD_URL = 'https://api-takumi.mihoyo.com/event/bbs_sign_reward/home?act_id={}'.format(ACT_ID)
    SIGN_URL = 'https://api-takumi.mihoyo.com/event/bbs_sign_reward/sign'

    def get_header(self):
        client_type, app_version, ds = get_ds('5')
        header = super().get_header()
        header.update({
            'User-Agent': self.USER_AGENT.format(app_version),
            'x-rpc-device_id': str(uuid.uuid3(uuid.NAMESPACE_URL, self._cookie)).replace(
                '-', '').upper(),
            'x-rpc-client_type': client_type,
            'x-rpc-app_version': app_version,
            'DS': ds
        })
        return header

    def get_roles(self):
        try:
            self.ROLES_INFO = request(
                'get', self.ROLE_URL, headers=super().get_header()).json()
        except Exception as e:
            raise Exception(e)
        return self.ROLES_INFO


class GenshinCheckin(__BaseCheckin):
    ACT_ID = 'e202102251931481'
    USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
    REFERER_URL = 'https://webstatic-sea.mihoyo.com/ys/event/signin-sea/index.html?act_id={}'.format(ACT_ID)
    INFO_URL = 'https://hk4e-api-os.mihoyo.com/event/sol/info?lang={}&act_id={}'.format(config.LANGUAGE, ACT_ID)
    REWARD_URL = 'https://hk4e-api-os.mihoyo.com/event/sol/home?lang={}&act_id={}'.format(config.LANGUAGE, ACT_ID)
    SIGN_URL = 'https://hk4e-api-os.mihoyo.com/event/sol/sign?lang={}'.format(config.LANGUAGE)
