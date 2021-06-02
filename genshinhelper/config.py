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
            self.config_json = json.load(f)

        # Language
        self.LANGUAGE = self.get_config('LANGUAGE')

        # Cookie configs
        # Cookie from https://bbs.mihoyo.com/ys/
        self.COOKIE_MIHOYOBBS = self.get_config('COOKIE_MIHOYOBBS')
        self.COOKIE_MIYOUBI = self.get_config('COOKIE_MIYOUBI')

        # Cookie from https://webstatic-sea.mihoyo.com/ys/event/signin-sea/index.html?act_id=e202102251931481&lang=en-us
        self.COOKIE_HOYOLAB = self.get_config('COOKIE_HOYOLAB')

        # Parameters from Sina Weibo intl. app.   aid=xxx; gsid=xxx; s=xxx
        self.COOKIE_WEIBO = self.get_config('COOKIE_WEIBO')

        # Cookie from https://m.weibo.cn
        self.COOKIE_KA = self.get_config('COOKIE_KA')

        # Notifier configs
        # iOS Bark App
        self.BARK_KEY = self.config_json.get('BARK_KEY')
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

        self.BARK_SOUND = self.get_config('BARK_SOUND')

        # Cool Push
        self.COOL_PUSH_SKEY = self.get_config('COOL_PUSH_SKEY')
        self.COOL_PUSH_MODE = self.get_config('COOL_PUSH_MODE')

        # Custom Notifier Config
        self.CUSTOM_NOTIFIER = self.get_config('CUSTOM_NOTIFIER')

        # DingTalk Bot
        self.DD_BOT_TOKEN = self.get_config('DD_BOT_TOKEN')
        self.DD_BOT_SECRET = self.get_config('DD_BOT_SECRET')

        # Discord webhook
        self.DISCORD_WEBHOOK = self.get_config('DISCORD_WEBHOOK')

        # iGot
        self.IGOT_KEY = self.get_config('IGOT_KEY')

        # pushplus
        self.PUSH_PLUS_TOKEN = self.get_config('PUSH_PLUS_TOKEN')
        self.PUSH_PLUS_USER = self.get_config('PUSH_PLUS_USER')

        # Server Chan
        self.SCKEY = self.get_config('SCKEY')
        self.SCTKEY = self.get_config('SCTKEY')

        # Telegram Bot
        self.TG_BOT_API = self.get_config('TG_BOT_API')
        self.TG_BOT_TOKEN = self.get_config('TG_BOT_TOKEN')
        self.TG_USER_ID = self.get_config('TG_USER_ID')

        # WeChat Work App
        self.WW_ID = self.get_config('WW_ID')
        self.WW_APP_SECRET = self.get_config('WW_APP_SECRET')
        self.WW_APP_USERID = self.get_config('WW_APP_USERID')
        self.WW_APP_AGENTID = self.get_config('WW_APP_AGENTID')

        # WeChat Work Bot
        self.WW_BOT_KEY = self.get_config('WW_BOT_KEY')

    def get_config(self, name: str):
        value = os.environ[name] if os.environ.get(name) else self.config_json.get(name, '')
        return value


config = Config()
