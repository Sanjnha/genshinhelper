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
        self.LANGUAGE = os.environ['LANGUAGE'] if 'LANGUAGE' in os.environ else config_json['language']

        # Cookie configs
        # Cookie from https://bbs.mihoyo.com/ys/
        self.COOKIE_MIHOYOBBS = os.environ['COOKIE_MIHOYOBBS'] if 'COOKIE_MIHOYOBBS' in os.environ else config_json['cookies']['cookie_mihoyobbs']

        # Cookie from https://www.hoyolab.com/genshin/
        self.COOKIE_HOYOLAB = os.environ['COOKIE_HOYOLAB'] if 'COOKIE_HOYOLAB' in os.environ else config_json['cookies']['cookie_hoyolab']

        # Cookie from https://m.weibo.cn
        self.COOKIE_WEIBO = os.environ['COOKIE_WEIBO'] if 'COOKIE_WEIBO' in os.environ else config_json['cookies']['cookie_weibo']
        self.WEIBO_INTL_AID = os.environ['WEIBO_INTL_AID'] if 'WEIBO_INTL_AID' in os.environ else config_json['cookies']['weibo_intl_aid']
        self.WEIBO_INTL_S = os.environ['WEIBO_INTL_S'] if 'WEIBO_INTL_S' in os.environ else config_json['cookies']['weibo_intl_s']

        # Cookie from https://ka.sina.com.cn
        self.COOKIE_KA = os.environ['COOKIE_KA'] if 'COOKIE_KA' in os.environ else config_json['cookies']['cookie_ka']

        # Notifier configs
        # iOS Bark App
        self.BARK_KEY = config_json['notifiers']['bark_key']
        if 'BARK_KEY' in os.environ:
            # Customed server
            if os.environ['BARK_KEY'].find(
                    'https') != -1 or os.environ['BARK_KEY'].find('http') != -1:
                self.BARK_KEY = os.environ['BARK_KEY']
            else:
                self.BARK_KEY = f"https://api.day.app/{os.environ['BARK_KEY']}"
        # Official server
        elif self.BARK_KEY and self.BARK_KEY.find('https') == -1 and self.BARK_KEY.find('http') == -1:
            self.BARK_KEY = f'https://api.day.app/{self.BARK_KEY}'
        self.BARK_SOUND = os.environ['BARK_SOUND'] if 'BARK_SOUND' in os.environ else config_json['notifiers'][
            'bark_sound']

        # Cool Push
        self.COOL_PUSH_SKEY = os.environ['COOL_PUSH_SKEY'] if 'COOL_PUSH_SKEY' in os.environ else config_json['notifiers']['cool_push_skey']
        self.COOL_PUSH_MODE = os.environ['COOL_PUSH_MODE'] if 'COOL_PUSH_MODE' in os.environ else config_json['notifiers']['cool_push_mode']

        # Custom Notifier Config
        self.CUSTOM_NOTIFIER = os.environ['CUSTOM_NOTIFIER'] if 'CUSTOM_NOTIFIER' in os.environ else config_json['notifiers']['custom_notifier']

        # DingTalk Bot
        self.DD_BOT_TOKEN = os.environ['DD_BOT_TOKEN'] if 'DD_BOT_TOKEN' in os.environ else config_json['notifiers']['dingtalk_bot_token']
        self.DD_BOT_SECRET = os.environ['DD_BOT_SECRET'] if 'DD_BOT_SECRET' in os.environ else config_json['notifiers']['dingtalk_bot_secret']

        # Discord webhook
        self.DISCORD_WEBHOOK = os.environ['DISCORD_WEBHOOK'] if 'DISCORD_WEBHOOK' in os.environ else config_json['notifiers']['discord_webhook']

        # iGot
        self.IGOT_KEY = os.environ['IGOT_KEY'] if 'IGOT_KEY' in os.environ else config_json['notifiers']['igot_key']

        # pushplus
        self.PUSH_PLUS_TOKEN = os.environ['PUSH_PLUS_TOKEN'] if 'PUSH_PLUS_TOKEN' in os.environ else config_json['notifiers']['push_plus_token']
        self.PUSH_PLUS_USER = os.environ['PUSH_PLUS_USER'] if 'PUSH_PLUS_USER' in os.environ else config_json['notifiers']['push_plus_user']

        # Server Chan
        self.SCKEY = os.environ['SCKEY'] if 'SCKEY' in os.environ else config_json['notifiers']['server_chan_key']
        self.SCTKEY = os.environ['SCTKEY'] if 'SCTKEY' in os.environ else config_json['notifiers']['server_chan_turbo_key']

        # Telegram Bot
        self.TG_BOT_API = os.environ['TG_BOT_API'] if 'TG_BOT_API' in os.environ else config_json['notifiers']['telegram_bot_api']
        self.TG_BOT_TOKEN = os.environ['TG_BOT_TOKEN'] if 'TG_BOT_TOKEN' in os.environ else config_json['notifiers']['telegram_bot_token']
        self.TG_USER_ID = os.environ['TG_USER_ID'] if 'TG_USER_ID' in os.environ else config_json['notifiers']['telegram_user_id']

        # WeChat Work App
        self.WW_ID = os.environ['WW_ID'] if 'WW_ID' in os.environ else config_json['notifiers']['wechat_work_id']
        self.WW_APP_SECRET = os.environ['WW_APP_SECRET'] if 'WW_APP_SECRET' in os.environ else config_json['notifiers']['wechat_work_app_secret']
        self.WW_APP_USERID = os.environ['WW_APP_USERID'] if 'WW_APP_USERID' in os.environ else config_json['notifiers']['wechat_work_app_userid']
        self.WW_APP_AGENTID = os.environ['WW_APP_AGENTID'] if 'WW_APP_AGENTID' in os.environ else config_json['notifiers']['wechat_work_app_agentid']

        # WeChat Work Bot
        self.WW_BOT_KEY = os.environ['WW_BOT_KEY'] if 'WW_BOT_KEY' in os.environ else config_json['notifiers']['wechat_work_bot_key']


config = Config()
