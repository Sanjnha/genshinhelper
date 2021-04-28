"""Configuration."""

import json
import os


class Config(object):
    """
    Get all configuration from the config.json file.
    If config.json dose not exist, use config.example.json file.

        Note:   Environment variables have a higher priority,
                if you set a environment variable in your system,
                that variable in the config.json file will be invalid.
    """

    def __init__(self):
        # Open and read the config file
        # project_path = os.path.dirname(os.path.dirname(__file__))
        project_path = os.path.dirname(__file__)
        config_file = os.path.join(project_path, 'config', 'config.json')
        if not os.path.exists(config_file):
            config_file = os.path.join(project_path, 'config', 'config.example.json')

        with open(config_file, 'r', encoding='utf-8') as f:
            config_json = json.load(f)

        # Language
        self.LANGUAGE = os.environ['LANGUAGE'] if os.environ.get('LANGUAGE') else config_json['language']

        # Cookie configs
        # Cookie from https://bbs.mihoyo.com/ys/
        self.COOKIE_MIHOYOBBS = os.environ['COOKIE_MIHOYOBBS'] if os.environ.get('COOKIE_MIHOYOBBS') else config_json['cookies']['cookie_mihoyobbs']

        # Cookie from https://www.hoyolab.com/genshin/
        self.COOKIE_HOYOLAB = os.environ['COOKIE_HOYOLAB'] if os.environ.get('COOKIE_HOYOLAB') else config_json['cookies']['cookie_hoyolab']

        # Cookie from https://m.weibo.cn
        self.COOKIE_WEIBO = os.environ['COOKIE_WEIBO'] if os.environ.get('COOKIE_WEIBO') else config_json['cookies']['cookie_weibo']
        self.WEIBO_INTL_AID = os.environ['WEIBO_INTL_AID'] if os.environ.get('WEIBO_INTL_AID') else config_json['cookies']['weibo_intl_aid']
        self.WEIBO_INTL_S = os.environ['WEIBO_INTL_S'] if os.environ.get('WEIBO_INTL_S') else config_json['cookies']['weibo_intl_s']

        # Cookie from https://ka.sina.com.cn
        self.COOKIE_KA = os.environ['COOKIE_KA'] if os.environ.get('COOKIE_KA') else config_json['cookies']['cookie_ka']

        # Notifier configs
        # iOS Bark App
        self.BARK_KEY = config_json['notifiers']['bark_key']
        if os.environ.get('BARK_KEY'):
            # Customed server
            if os.environ['BARK_KEY'].find(
                    'https') != -1 or os.environ['BARK_KEY'].find('http') != -1:
                self.BARK_KEY = os.environ['BARK_KEY']
            else:
                self.BARK_KEY = f"https://api.day.app/{os.environ['BARK_KEY']}"
        # Official server
        elif self.BARK_KEY and self.BARK_KEY.find('https') == -1 and self.BARK_KEY.find('http') == -1:
            self.BARK_KEY = f'https://api.day.app/{self.BARK_KEY}'

        self.BARK_SOUND = os.environ['BARK_SOUND'] if os.environ.get('BARK_SOUND') else config_json['notifiers'][
            'bark_sound']

        # Cool Push
        self.COOL_PUSH_SKEY = os.environ['COOL_PUSH_SKEY'] if os.environ.get('COOL_PUSH_SKEY') else config_json['notifiers']['cool_push_skey']
        self.COOL_PUSH_MODE = os.environ['COOL_PUSH_MODE'] if os.environ.get('COOL_PUSH_MODE') else config_json['notifiers']['cool_push_mode']

        # Custom Notifier Config
        self.CUSTOM_NOTIFIER = os.environ['CUSTOM_NOTIFIER'] if os.environ.get('CUSTOM_NOTIFIER') else config_json['notifiers']['custom_notifier']

        # DingTalk Bot
        self.DD_BOT_TOKEN = os.environ['DD_BOT_TOKEN'] if os.environ.get('DD_BOT_TOKEN') else config_json['notifiers']['dingtalk_bot_token']
        self.DD_BOT_SECRET = os.environ['DD_BOT_SECRET'] if os.environ.get('DD_BOT_SECRET') else config_json['notifiers']['dingtalk_bot_secret']

        # Discord webhook
        self.DISCORD_WEBHOOK = os.environ['DISCORD_WEBHOOK'] if os.environ.get('DISCORD_WEBHOOK') else config_json['notifiers']['discord_webhook']

        # iGot
        self.IGOT_KEY = os.environ['IGOT_KEY'] if os.environ.get('IGOT_KEY') else config_json['notifiers']['igot_key']

        # pushplus
        self.PUSH_PLUS_TOKEN = os.environ['PUSH_PLUS_TOKEN'] if os.environ.get('PUSH_PLUS_TOKEN') else config_json['notifiers']['push_plus_token']
        self.PUSH_PLUS_USER = os.environ['PUSH_PLUS_USER'] if os.environ.get('PUSH_PLUS_USER') else config_json['notifiers']['push_plus_user']

        # Server Chan
        self.SCKEY = os.environ['SCKEY'] if os.environ.get('SCKEY') else config_json['notifiers']['server_chan_key']
        self.SCTKEY = os.environ['SCTKEY'] if os.environ.get('SCTKEY') else config_json['notifiers']['server_chan_turbo_key']

        # Telegram Bot
        self.TG_BOT_API = os.environ['TG_BOT_API'] if os.environ.get('TG_BOT_API') else config_json['notifiers']['telegram_bot_api']
        self.TG_BOT_TOKEN = os.environ['TG_BOT_TOKEN'] if os.environ.get('TG_BOT_TOKEN') else config_json['notifiers']['telegram_bot_token']
        self.TG_USER_ID = os.environ['TG_USER_ID'] if os.environ.get('TG_USER_ID') else config_json['notifiers']['telegram_user_id']

        # WeChat Work App
        self.WW_ID = os.environ['WW_ID'] if os.environ.get('WW_ID') else config_json['notifiers']['wechat_work_id']
        self.WW_APP_SECRET = os.environ['WW_APP_SECRET'] if os.environ.get('WW_APP_SECRET') else config_json['notifiers']['wechat_work_app_secret']
        self.WW_APP_USERID = os.environ['WW_APP_USERID'] if os.environ.get('WW_APP_USERID') else config_json['notifiers']['wechat_work_app_userid']
        self.WW_APP_AGENTID = os.environ['WW_APP_AGENTID'] if os.environ.get('WW_APP_AGENTID') else config_json['notifiers']['wechat_work_app_agentid']

        # WeChat Work Bot
        self.WW_BOT_KEY = os.environ['WW_BOT_KEY'] if os.environ.get('WW_BOT_KEY') else config_json['notifiers']['wechat_work_bot_key']


config = Config()
