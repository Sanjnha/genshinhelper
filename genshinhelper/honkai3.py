import json
import time
import uuid

from .utils import MESSAGE_TEMPLATE, log, request, _


class Bh3Checkin(object):
    ACT_ID = 'e202104072769'
    USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.8.0'
    REFERER_URL = 'https://webstatic.mihoyo.com/bh3/event/euthenia/index.html?bbs_presentation_style={}&bbs_game_role_required={}&bbs_auth_required={}&act_id={}&utm_source={}&utm_medium={}&utm_campaign={}'.format(
        'fullscreen', 'bh3_cn', 'true', ACT_ID, 'bbs', 'mys', 'icon')
    ROLES_INFO = {}
    INFO_URL = ''
    ROLE_URL = 'https://api-takumi.mihoyo.com/binding/api/getUserGameRolesByCookie?game_biz={}'.format(
        'bh3_cn')
    _INFO_URL = 'https://api-takumi.mihoyo.com/common/euthenia/index?region={}&act_id={}&uid={}'
    SIGN_URL = 'https://api-takumi.mihoyo.com/common/euthenia/sign'

    def __init__(self, cookie: str=None):
        self._cookie = cookie
        self._sign_data = {}

    def get_header(self):
        header = {
            'Cookie':
            self._cookie,
            'User-Agent':
            self.USER_AGENT,
            'Referer':
            self.REFERER_URL,
            'Accept-Encoding':
            'gzip, deflate, br',
            'x-rpc-device_id':
            str(uuid.uuid3(uuid.NAMESPACE_URL, self._cookie)).replace(
                '-', '').upper()
        }
        return header

    def get_weekly_finance(self, bind_uid, bind_region):
        # level > 25
        url = 'https://api.mihoyo.com/bh3-weekly_finance/api/index'
        payload = {
            'game_biz': 'bh3_cn',
            'bind_uid': bind_uid,
            'bind_region': bind_region
        }
        response = request(
            'get', url, headers=self.get_header(), params=payload).json()

        return response

    @property
    def roles_list(self):
        response = request(
            'get', self.ROLE_URL, headers=self.get_header()).json()

        if response.get('retcode', 1) != 0:
            raise Exception(response.get('message', 'Empty roles data'))

        roles_list = response.get('data', {}).get('list', [])
        return roles_list

    @property
    def _sign_info(self):
        response = request(
            'get', self.INFO_URL, headers=self.get_header()).json()
        return response

    def sign(self):
        sign_info = self._sign_info.get('data', {}).get('sign', {})

        today = sign_info.get('now', '1970-01-01 00:00:00').split(' ')[0]
        awards = sign_info.get('list', [])
        # 0: can not check in, 1: can check in, 2: already checked in
        current_day = len(awards) - [i['status'] for i in awards].count(0)
        total_sign_day = [i['status'] for i in awards].count(2)
        is_sign = True if awards[current_day - 1]['status'] == 2 else False
        region_name = self._sign_data.get('region_name', 'Global')
        uid = self._sign_data.get('uid', 123456789)
        hidden_uid = str(uid).replace(str(uid)[3:-3], '***', 1)
        data = self._sign_data.get('post_data', {})
        region = self._sign_data.get('region')

        travel_notes = '希望不熄 薪火永燃'
        weekly_finance = self.get_weekly_finance(uid, region)
        if weekly_finance.get('retcode', -9999) == 0:
            finance = weekly_finance.get('data', {})
            travel_notes = _('''舰长的 {} 月手帐
    💎水晶: {}
    🔮星石: {}''').format(finance['month'], finance['month_hcoin'],
                       finance['month_star'])

        message = {
            'today': today,
            'region_name': region_name,
            'uid': hidden_uid,
            'total_sign_day': total_sign_day,
            'travel_notes': travel_notes,
            'end': ''
        }

        log.info(_('准备为舰长 {hidden_uid} 签到...').format(hidden_uid=hidden_uid))
        time.sleep(5)

        if is_sign:
            message['award_name'] = awards[total_sign_day - 1].get('name')
            message['award_cnt'] = awards[total_sign_day - 1].get('cnt')
            message['status'] = _('👀 舰长, 你已经签到过了哦')

            return self.message.format(**message)
        else:
            message['award_name'] = awards[total_sign_day].get('name')
            message['award_cnt'] = awards[total_sign_day].get('cnt')

        try:
            response = request(
                'post',
                self.SIGN_URL,
                headers=self.get_header(),
                data=json.dumps(data, ensure_ascii=False)).json()
        except Exception as e:
            raise Exception(e)
        # 0:      success
        # -5003:  already checked in
        code = response.get('retcode', 99999)
        if code != 0:
            return response
        message['total_sign_day'] = total_sign_day + 1
        message['status'] = response.get('message')

        log.info(_('签到完毕'))
        return self.message.format(**message)

    def run(self):
        roles_list = self.roles_list
        if roles_list:
            result_list = []
            log.info(
                _('当前账号绑定了 {num_roles} 个角色').format(num_roles=len(roles_list)))
            for role in roles_list:

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
                result_list.append(self.sign())
            return ''.join(result_list)

    @property
    def message(self):
        return MESSAGE_TEMPLATE.replace('月', '周', 1)

