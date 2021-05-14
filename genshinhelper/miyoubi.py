import random
import time
import uuid

from .utils import log, request, get_ds


TOKEN_URL = 'https://api-takumi.mihoyo.com/auth/api/getMultiTokenByLoginTicket?login_ticket={}&token_types=3&uid={}'


def get_mybcookie(cookie):
    if 'stoken' in cookie:
        return cookie
    elif 'login_ticket' in cookie:
        try:
            stuid = cookie.split('account_id=')[1].split(';')[0]
            login_ticket = cookie.split('login_ticket=')[1].split(';')[0]
            url = TOKEN_URL.format(login_ticket, stuid)
            response = request('get', url).json()
        except Exception as e:
            raise Exception(e)
        else:
            if response.get('message') == 'OK':
                stoken = response['data']['list'][0]['token']
                mybcookie = f'stuid={stuid}; stoken={stoken}; login_ticket={login_ticket}'
                raise Exception('Your COOKIE_MIYOUBI:\n' + mybcookie)
            else:
                raise Exception('login_ticket已失效,请重新登录米游社获取')


class MiyoubiCheckin(object):
    SIGN_URL = 'https://bbs-api.mihoyo.com/apihub/sapi/signIn?gids={}'
    POST_LIST_URL = 'https://bbs-api.mihoyo.com/post/api/getForumPostList?forum_id={}&is_good=false&is_hot=false&page_size=20&sort_type=1'
    POST_FULL_URL = 'https://bbs-api.mihoyo.com/post/api/getPostFull?post_id={}'
    UPVOTE_URL = 'https://bbs-api.mihoyo.com/apihub/sapi/upvotePost'
    SHARE_URL = 'https://bbs-api.mihoyo.com/apihub/api/getShareConf?entity_id={}&entity_type=1'

    def __init__(self, cookie):
        self._cookie = get_mybcookie(cookie)
        self.message_box = []

    def get_header(self):
        client_type, app_version, ds = get_ds('android')
        header = {
            'Cookie':
            self._cookie,
            'User-Agent': 'okhttp/4.8.0',
            'Referer': 'https://app.mihoyo.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'x-rpc-channel': 'miyousheluodi',
            'x-rpc-device_model': 'Mi 10',
            'x-rpc-device_name': '',
            'x-rpc-device_id': str(uuid.uuid3(uuid.NAMESPACE_URL, self._cookie)).replace(
                '-', '').upper(),
            'x-rpc-sys_version': '6.0.1',
            'x-rpc-client_type': client_type,
            'x-rpc-app_version': app_version,
            'DS': ds
        }
        return header

    def sign(self, id):
        log.info('正在签到...')
        try:
            url = self.SIGN_URL.format(id)
            response = request('post', url, headers=self.get_header()).json()
        except Exception as e:
            raise Exception(e)
        else:
            if response.get('message') == 'OK' or '重复' in response.get('message'):
                log.info(f"社区签到: {response.get('message')}")
                self.message_box.append(f"社区签到: {response.get('message')}")
            else:
                raise Exception(f"社区签到: 失败 {response.get('message')}")

    def get_posts(self, forum_id):
        try:
            url = self.POST_LIST_URL.format(forum_id)
            response = request('get', url).json()
        except Exception as e:
            raise Exception(e)
        else:
            if response.get('message') == 'OK':
                post_list = response.get('data', {}).get('list', [])
                posts = [{
                    'post_id': post.get('post', {}).get('post_id'),
                    'title': post.get('post', {}).get('subject')
                } for post in post_list if post_list]
                return posts

    def view_post(self, post):
        log.info('正在看帖...')
        time.sleep(3)
        try:
            url = self.POST_FULL_URL.format(post['post_id'])
            response = request('get', url, headers=self.get_header()).json()
        except Exception as e:
            raise Exception(e)
        else:
            if response.get('message') == 'OK':
                log.info(f"看帖成功: {post['title']}")
                self.message_box.append('看帖成功')

    def upvote_post(self, post):
        log.info('正在点赞...')
        time.sleep(3)
        try:
            url = self.UPVOTE_URL
            data = {'post_id': post['post_id'], 'is_cancel': False}
            response = request(
                'post', url, json=data, headers=self.get_header()).json()
        except Exception as e:
            raise Exception(e)
        else:
            if response.get('message') == 'OK':
                log.info(f"点赞成功: {post['title']}")
                self.message_box.append('点赞成功')

    def share_post(self, post):
        log.info('正在分享...')
        try:
            url = self.SHARE_URL.format(post['post_id'])
            response = request('get', url, headers=self.get_header()).json()
        except Exception as e:
            raise Exception(e)
        else:
            if response.get('message') == 'OK':
                log.info(f"分享成功: {post['title']}")
                self.message_box.append('分享成功')

    def run(self):
        # 原神板块
        id = 2
        forum_id = 26

        self.sign(id)
        posts = self.get_posts(forum_id)
        [self.view_post(i) for i in random.sample(posts, 3)]
        [self.upvote_post(i) for i in random.sample(posts, 5)]
        [self.share_post(i) for i in random.sample(posts, 1)]

        return '\n    '.join(self.message_box)

