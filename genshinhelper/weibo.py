import re

from bs4 import BeautifulSoup

from .config import config
from .exceptions import CookiesExpired
from .utils import log, request


class SuperTopicCheckin(object):
    USER_AGENT = 'WeiboOverseas/4.1.4 (iPhone; iOS 14.0.1; Scale/2.00)'
    WEIBO_API = 'https://api.weibo.cn'
    FOLLOW_DATA_URL = WEIBO_API + '/2/cardlist'
    SIGN_URL = WEIBO_API + '/2/page/button'

    def __init__(self, cookie: str = None):
        self._cookie = cookie

    def get_header(self):
        header = {
            'User-Agent': self.USER_AGENT,
            'Cookie': self._cookie
        }
        return header

    def get_follow_data(self):
        try:
            url = self.FOLLOW_DATA_URL
            data = {
                'aid': config.WEIBO_INTL_AID,
                'c': 'weicoabroad',
                'containerid': '100803_-_followsuper',
                's': config.WEIBO_INTL_S,
                'ua': 'iPhone12%2C1_iOS14.0.1_Weibo_intl_4140_cell'
            }
            response = request(
                'get',
                url,
                params=data,
                headers=self.get_header(),
                verify=False).json()
        except Exception as e:
            raise Exception(f'Failed to get follow list:\n{e}')
        else:
            card_group = response.get('cards', [{}])[0].get('card_group', [])
            follow_list = [
                card for card in card_group if card.get('card_type') == '8'
            ]
            if not follow_list:
                return []

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
        if not follow_data:
            raise Exception('Empty follow data')

        message = []
        for follow in follow_data:
            name = follow.get('name')
            lv = follow.get('lv')
            is_sign = follow.get('is_sign')
            data = follow.get('sign_data', {})
            name_style = f'⚜️ [Lv.{lv}]{name}'

            # Already checked in
            if is_sign == '已签':
                message.append(f'{name_style} ☑️')
            elif is_sign == '签到':
                try:
                    url = self.SIGN_URL
                    response = request(
                        'get', url, params=data, headers=self.get_header(), verify=False).json()
                except Exception as e:
                    raise Exception(f'Failed to run sign:\n{e}')
                else:
                    if response.get('result') in (1, '1'):
                        message.append(f'{name_style} ✅')
                    # Already checked in
                    elif '已签到' in response.get('msg', ''):
                        message.append(f'{name_style} ☑️')
                    # Verification required
                    # elif response.get('result') == 0 and response.get('scheme'):
                    #     log.error(f'Failed to run sign:\nVerification required.')
                    else:
                        raise Exception(f'{name_style} :Failed to run sign:\n{response}')

            else:
                log.info('Unknown check-in status')

        return '\n    '.join(message)


class RedemptionCode(object):
    USER_AGENT = 'WeiboOverseas/4.1.4 (iPhone; iOS 14.0.1; Scale/2.00)'
    CONTAINER_ID = '100808fc439dedbb06ca5fd858848e521b8716'
    GENSHIN_CHAOHUA_URL = 'https://m.weibo.cn/api/container/getIndex?containerid={}_-_feed'.format(CONTAINER_ID)
    DRAW_URL = 'https://ka.sina.com.cn/innerapi/draw'
    MYBOX_URL = 'https://ka.sina.com.cn/html5/mybox'

    def __init__(self, cookie: str = None):
        self._cookie = cookie

    def get_header(self):
        header = {
            'User-Agent': self.USER_AGENT,
            'Referer': 'https://m.weibo.cn',
            'Cookie': self._cookie
        }
        return header

    @property
    def event_gift_ids(self):
        try:
            url = self.GENSHIN_CHAOHUA_URL
            response = request('get', url, headers=self.get_header()).json()
        except Exception as e:
            raise Exception(f'Failed to get event information:\n{e}')
        else:
            cards = response.get('data', {}).get('cards', [])
            event_card = [
                card for card in cards if card.get('itemid') == 'pagemanual_2'
            ]
            if not event_card:
                return []

            group = event_card[0].get('card_group', [{}])[0].get('group', [])

            ids = [i for item in group if '签到' in item.get('title_sub') for i in re.findall('gift/(\d*)', item['scheme'])]
            return ids

    @property
    def mybox_codes(self):
        header = self.get_header()
        header['Referer'] = 'https://ka.sina.com.cn/html5/'
        try:
            url = self.MYBOX_URL
            response = request(
                'get', url, headers=header, allow_redirects=False)
        except Exception as e:
            raise Exception(f'Failed to get mybox codes:\n{e}')
        else:
            mybox_codes = []
            if response.status_code == 200:
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')
                # print(soup.prettify())
                boxs = soup.find_all(class_='giftbag')

                for box in boxs:
                    item = {
                        'id': box.find(class_='deleBtn').get('data-itemid'),
                        'title': box.find(class_='title itemTitle').text,
                        'code': box.find('span').parent.contents[1]
                    }
                    mybox_codes.append(item)

            elif response.status_code == 302 or 500:
                raise CookiesExpired('😳 ka.sina: 登录可能失效, 尝试重新登录')
            else:
                raise Exception('😳 ka.sina: 个人中心兑换码获取失败')
            return mybox_codes

    @property
    def mybox_gift_ids(self):
        ids = [item.get('id') for item in self.mybox_codes]
        return ids

    @property
    def unclaimed_gift_ids(self):
        event_gift_ids = self.event_gift_ids
        if not event_gift_ids:
            return []

        mybox_gift_ids = self.mybox_gift_ids
        ids = [i for i in event_gift_ids if i not in mybox_gift_ids]
        return ids

    def get_code(self, id):
        header = self.get_header()
        header['Referer'] = f'https://ka.sina.com.cn/html5/gift/{id}'
        data = {'gid': 10725, 'itemId': id, 'channel': 'wblink'}

        try:
            url = self.DRAW_URL
            response = request(
                'get', url, params=data, headers=header).json()
        except Exception as e:
            raise Exception(f'Failed to get redemption code with ID {id}:\n{e}')
        else:
            if response.get('k'):
                log.info(f'{id} 的兑换码领取成功')
                return response['data']['kahao']
            elif response.get('code') == '2002' and '头像' in response.get(
                    'msg', ''):
                raise Exception(f'🥳 {id}: 每天只能领取一张或该兑换码已经领取过了哦')
            elif response.get('code') == '2002':
                raise Exception(f'😳 {id}: {response["msg"]}')
            elif 'login' in response.get('msg', ''):
                raise Exception('登录失效, 请重新登录')
            else:
                raise Exception(f'😳 {id}: {response}')

    def run(self):
        ids = self.unclaimed_gift_ids
        codes = []
        if not ids:
            msg = '没有未领取的兑换码'
            log.info(msg)
            codes.append(msg)
        else:
            log.info(f'检测到有 {len(ids)} 个未领取的兑换码')

            for id in ids:
                code = self.get_code(id)
                if code:
                    codes.append(code)
        return '\n    '.join(codes)
