import random
import time
import uuid

from .exceptions import GenshinHelperException
from .utils import log, request, get_ds, extract_cookie


TOKEN_URL = 'https://api-takumi.mihoyo.com/auth/api/getMultiTokenByLoginTicket?login_ticket={}&token_types=3&uid={}'


def get_app_cookie(cookie):
    if 'stoken' in cookie:
        return cookie

    login_ticket = extract_cookie('login_ticket', cookie)
    stuid = extract_cookie('account_id', cookie)
    url = TOKEN_URL.format(login_ticket, stuid)
    response = request('get', url).json()
    if response.get('message') != 'OK':
        raise GenshinHelperException('Failed to get multi token: '
            'The cookie seems to be invalid, please re-login to bbs.mihoyo.com')

    stoken = response['data']['list'][0]['token']
    app_cookie = f'stuid={stuid}; stoken={stoken}; login_ticket={login_ticket}'
    raise GenshinHelperException(f'YOUR COOKIE_MIYOUBI:\n{app_cookie}')


class MiyoubiCheckin(object):
    STATE_URL = 'https://bbs-api.mihoyo.com/apihub/sapi/getUserMissionsState'
    SIGN_URL = 'https://bbs-api.mihoyo.com/apihub/sapi/signIn?gids={}'
    POST_LIST_URL = 'https://bbs-api.mihoyo.com/post/api/getForumPostList?forum_id={}&is_good=false&is_hot=false&page_size=20&sort_type=1'
    POST_FULL_URL = 'https://bbs-api.mihoyo.com/post/api/getPostFull?post_id={}'
    UPVOTE_URL = 'https://bbs-api.mihoyo.com/apihub/sapi/upvotePost'
    SHARE_URL = 'https://bbs-api.mihoyo.com/apihub/api/getShareConf?entity_id={}&entity_type=1'

    def __init__(self, cookie: str):
        self._cookie = get_app_cookie(cookie)
        self.get_missions_state()

    def get_header(self):
        client_type, app_version, ds = get_ds('android')
        header = {
            'Cookie': self._cookie,
            'User-Agent': 'okhttp/4.8.0',
            'Referer': 'https://app.mihoyo.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'x-rpc-channel': 'miyousheluodi',
            'x-rpc-device_id': str(uuid.uuid3(uuid.NAMESPACE_URL, self._cookie)).replace(
                '-', '').upper(),
            'x-rpc-client_type': client_type,
            'x-rpc-app_version': app_version,
            'DS': ds
        }
        return header

    def get_missions_state(self):
        url = self.STATE_URL
        response = request('get', url, headers=self.get_header()).json()
        self.total_points = response.get('data', {}).get('total_points', -1)
        states = response.get('data', {}).get('states', [])
        self.missions_state = {
            i['mission_key']: i['is_get_award'] for i in states if i['mission_id'] in (58, 59, 60, 61)
        }
        self.is_sign = self.missions_state.get('continuous_sign', False)
        self.is_view = self.missions_state.get('view_post_0', False)
        self.is_upvote = self.missions_state.get('post_up_0', False)
        self.is_share = self.missions_state.get('share_post_0', False)

    def sign(self, id: int):
        forums = {1: '崩坏3', 2: '原神', 3: '崩坏2', 4: '未定事件簿', 5: '大别野'}
        if id not in range(1, 6):
            raise ValueError('The value of id is one of 1, 2, 3, 4, 5')

        url = self.SIGN_URL.format(id)
        response = request('post', url, headers=self.get_header()).json()
        message = response.get('message')
        result = (False, message)
        if message == 'OK' or '重复' in message:
            result = (True, message)

        log.info(f'{forums[id]}: {message}')
        return result

    def get_posts(self, forum_id: int):
        # 1: 崩坏3  26: 原神  30: 崩坏2  37: 未定事件簿  34: 大别野
        forum_ids = (1, 26, 30, 37, 34)
        if forum_id not in forum_ids:
            raise ValueError('The value of forum_id is one of 1, 26, 30, 37, 34')

        url = self.POST_LIST_URL.format(forum_id)
        response = request('get', url).json()
        message = response.get('message')
        if message != 'OK':
            raise GenshinHelperException(f'Failed to get posts:\n{message}')

        post_list = response.get('data', {}).get('list', [])
        posts = [{
            'post_id': post.get('post', {}).get('post_id', 0),
            'title': post.get('post', {}).get('subject', 'untitled')
        } for post in post_list if post_list]

        log.info(f'Succeeded in getting {len(posts)} posts')
        return posts

    def view_post(self, post: dict):
        time.sleep(3)
        post_id = post.get('post_id')
        title = post.get('title')
        url = self.POST_FULL_URL.format(post_id)
        response = request('get', url, headers=self.get_header()).json()
        message = response.get('message')
        result = (False, title)
        if message == 'OK':
            result = (True, title)

        log.info(f'{title}: {message}')
        return result

    def upvote_post(self, post: dict):
        time.sleep(3)
        post_id = post.get('post_id')
        title = post.get('title')
        url = self.UPVOTE_URL
        data = {'post_id': post_id, 'is_cancel': False}
        response = request('post', url, json=data, headers=self.get_header()).json()
        message = response.get('message')
        result = (False, title)
        if message == 'OK':
            result = (True, title)

        log.info(f'{title}: {message}')
        return result

    def share_post(self, post: dict):
        post_id = post.get('post_id')
        title = post.get('title')
        url = self.SHARE_URL.format(post_id)
        response = request('get', url, headers=self.get_header()).json()
        message = response.get('message')
        result = (False, title)
        if message == 'OK':
            result = (True, title)

        log.info(f'{title}: {message}')
        return result

    def run(self):
        def get_result(name, info):
            return f'{name} ({[i[0] for i in info].count(True)}/{len(info)})'

        log.info(f'🌕 {self.total_points}')
        log.info('Preparing to get posts...')
        forum_id = 26
        posts = self.get_posts(forum_id)

        log.info('Preparing to check-in...')
        sign = [self.sign(i) for i in range(1, 6) if not self.is_sign]
        log.info('Preparing to view posts...')
        view = [self.view_post(i) for i in random.sample(posts[0:5], 3) if not self.is_view]
        log.info('Preparing to upvote posts...')
        upvote = [self.upvote_post(i) for i in random.sample(posts[5:17], 10) if not self.is_upvote]
        log.info('Preparing to share post...')
        share = [self.share_post(i) for i in random.sample(posts[-3:-1], 1) if not self.is_share]

        message_box = [
            get_result('签到', sign),
            get_result('浏览', view),
            get_result('点赞', upvote),
            get_result('分享', share)
        ]

        return '\n    '.join(message_box)
      
