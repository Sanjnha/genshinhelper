import re
import requests

from bs4 import BeautifulSoup

from . import notifiers
from .config import config
from .exceptions import GenshinHelperException
from .utils import log, request, extract_cookie


class SuperTopicCheckin(object):
    USER_AGENT = 'WeiboOverseas/4.1.4 (iPhone; iOS 14.0.1; Scale/2.00)'
    WEIBO_API = 'https://api.weibo.cn'
    FOLLOW_DATA_URL = WEIBO_API + '/2/cardlist'
    SIGN_URL = WEIBO_API + '/2/page/button'

    def __init__(self, cookie: str = None):
        self._cookie = cookie
        self._cookie_wb = config.COOKIE_KA
        self.headers = {
            'User-Agent': self.USER_AGENT,
            'Cookie': self._cookie_wb
        }

    def get_follow_data(self):
        url = self.FOLLOW_DATA_URL
        data = {
            'containerid': '100803_-_followsuper',
            'c': 'weicoabroad',
            's': extract_cookie('s', self._cookie),
            'gsid': extract_cookie('gsid', self._cookie),
            'aid': extract_cookie('aid', self._cookie),   # ios
            'from': extract_cookie('from', self._cookie)  # android
        }
        # turn off certificate verification
        response = request('get', url, params=data, headers=self.headers, verify=False).json()
        errno = response.get('errno')
        if errno:
            raise GenshinHelperException(f'Failed to get follow super:\n{response}')

        card_group = response.get('cards', [{}])[0].get('card_group', [])
        follow_list = [
            card for card in card_group if card.get('card_type') == '8'
        ]
        if not follow_list:
            raise GenshinHelperException('Failed to get follow list, '
            'please make sure you have followed the Genshin Impact super topic.')

        follow_data = []
        for item in follow_list:
            action = item.get('buttons', [{}])[0].get('params', {}).get(
                'action', '')
            request_url = ''.join(
                re.findall('(?<=request_url=)(.*)%26container', action))
            sign_data = {k: v for (k, v) in data.items()}
            del sign_data['containerid']
            sign_data['request_url'] = request_url

            follow = {
                'name': item.get('title_sub'),
                'lv': int(re.findall('\d+', item.get('desc1', '0'))[0]),
                'is_sign': item.get('buttons', [{}])[0].get('name'),
                'sign_data': sign_data
            }
            follow_data.append(follow)

        follow_data.sort(key=lambda k: (k.get('lv', 0)), reverse=True)

        return follow_data

    def run(self):
        follow_data = self.get_follow_data()
        message_box = []
        for follow in follow_data:
            name = follow.get('name')
            lv = follow.get('lv')
            is_sign = follow.get('is_sign')
            data = follow.get('sign_data', {})
            name_style = f'⚜️ [Lv.{lv}]{name}'

            # Already checked in
            if is_sign == '已签':
                message_box.append(f'{name_style} ☑️')
            elif is_sign == '签到':
                url = self.SIGN_URL
                # turn off certificate verification
                response = request('get', url, params=data, headers=self.headers, verify=False).json()
                if response.get('result') in (1, '1'):
                    message_box.append(f'{name_style} ✅')
                # Already checked in
                elif '已签到' in response.get('msg', ''):
                    message_box.append(f'{name_style} ☑️')
                else:
                    raise GenshinHelperException(f'{name_style} :Failed to run sign:\n{response}')
            else:
                raise GenshinHelperException('Unknown check-in status')

        return '\n    '.join(message_box)


class RedemptionCode(object):
    USER_AGENT = 'WeiboOverseas/4.1.4 (iPhone; iOS 14.0.1; Scale/2.00)'
    CONTAINER_ID = '100808fc439dedbb06ca5fd858848e521b8716'
    GENSHIN_CHAOHUA_URL = 'https://m.weibo.cn/api/container/getIndex?containerid={}_-_feed'.format(CONTAINER_ID)
    DRAW_URL = 'https://ka.sina.com.cn/innerapi/draw'
    MYBOX_URL = 'https://ka.sina.com.cn/html5/mybox'

    def __init__(self, cookie: str = None):
        self._cookie = self.get_ka_cookie(cookie)
        self.headers = {
            'User-Agent': self.USER_AGENT,
            'Referer': 'https://ka.sina.com.cn/html5'
        }

    @staticmethod
    def get_ka_cookie(cookie):
        SUB = extract_cookie('SUB', cookie)
        SUBP = extract_cookie('SUBP', cookie)

        session = requests.session()
        session.get('https://ka.sina.com.cn/html5')
        jar = requests.cookies.RequestsCookieJar()
        jar.set('SUB', SUB)
        jar.set('SUBP', SUBP)
        session.cookies.update(jar)
        cookie_ka = session.cookies.get_dict()
        return cookie_ka

    @property
    def event_gift_ids(self):
        is_event = self.check_event()
        if not is_event:
            return []

        group = self.event_card[0].get('card_group', [{}])[0].get('group', [])
        ids = [i for item in group if '签到' in item.get('title_sub') for i in re.findall(
            'gift/(\d*)', item['scheme'])]
        return ids

    @property
    def mybox_codes(self):
        url = self.MYBOX_URL
        response = request(
            'get', url, headers=self.headers, cookies=self._cookie, allow_redirects=False)
        if response.status_code != 200:
            raise GenshinHelperException('Failed to get my box codes: '
            'The cookie seems to be invalid, please re-login to m.weibo.cn')

        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup.prettify())
        boxs = soup.find_all(class_='giftbag')
        mybox_codes = []
        for box in boxs:
            item = {
                'id': box.find(class_='deleBtn').get('data-itemid'),
                'title': box.find(class_='title itemTitle').text,
                'code': box.find('span').parent.contents[1]
            }
            mybox_codes.append(item)

        return mybox_codes

    @property
    def mybox_gift_ids(self):
        mybox_codes = self.gift_bag = self.mybox_codes
        ids = [item.get('id') for item in mybox_codes]
        return ids

    @property
    def unclaimed_gift_ids(self):
        event_gift_ids = self.event_gift_ids
        mybox_gift_ids = self.mybox_gift_ids
        ids = [i for i in event_gift_ids if i not in mybox_gift_ids]
        return ids

    def check_event(self, subscribe = False):
        url = self.GENSHIN_CHAOHUA_URL
        response = request('get', url, headers=self.headers).json()
        cards = response.get('data', {}).get('cards', [])
        event_card = [
            card for card in cards if card.get('itemid') == 'pagemanual_2'
        ]
        if not event_card:
            return False

        if subscribe:
            message = (
                '原神超话签到提醒',
                '亲爱的旅行者，原神微博超话签到活动现已开启，请注意活动时间！如已完成任务，请忽略本信息。'
            )
            notifiers.send2all(status=message[0], desp=message[1])

        self.event_card = event_card
        return True

    def get_code(self, id):
        headers = self.headers
        headers['Referer'] = f'https://ka.sina.com.cn/html5/gift/{id}'
        url = self.DRAW_URL
        data = {'gid': 10725, 'itemId': id, 'channel': 'wblink'}
        response = request('get', url, params=data, headers=headers, cookies=self._cookie).json()

        if response.get('k'):
            log.info(f'The redemption code of ID {id} received successfully')
            return response['data']['kahao']
        elif response.get('code') == '2002' and '头像' in response.get('msg', ''):
            log.error(f'{id}: You can only receive one redemption code per day '
            'or the code has already been received!')
        elif response.get('code') == '2002':
            log.error(f'Failed to get code with ID {id}: {response["msg"]}')
        elif 'login' in response.get('msg', ''):
            raise GenshinHelperException('Failed to get code: '
            'The cookie seems to be invalid, please re-login to m.weibo.cn')
        else:
            log.error(f'Failed to get code with ID {id}: {response}')

        return f'{id}: {response["msg"]}'

    def run(self):
        is_event = self.check_event(subscribe = True)
        if not is_event:
            message = '原神超话现在没有活动哦'
            return message

        ids = self.unclaimed_gift_ids
        if not ids:
            recent_codes = ' *'.join([f"{i['title']} {i['code']}" for i in self.gift_bag[:3]])
            message = f'原神超话签到活动已开启，但是没有未领取的兑换码。\n    最近 3 个码: {recent_codes}'
            return message

        log.info(f'检测到有 {len(ids)} 个未领取的兑换码')
        codes = [self.get_code(id) for id in ids]
        return '\n    '.join(codes)

