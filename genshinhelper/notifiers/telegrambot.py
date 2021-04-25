from .basenotifier import BaseNotifier as Base
from ..config import config


class TelegramBot(Base):
    def __init__(self):
        self.name = 'Telegram Bot'
        self.token = config.TG_BOT_TOKEN if config.TG_BOT_TOKEN and config.TG_USER_ID else ''
        self.retcode_key = 'ok'
        self.retcode_value = 'error_code'

    def send(self, text=Base.app, status=Base.status, desp=Base.desp):
        url = f'https://{config.TG_BOT_API}/bot{config.TG_BOT_TOKEN}/sendMessage'
        data = {
            'chat_id': config.TG_USER_ID,
            'text': f'{text} {status}\n\n{desp}',
            'disable_web_page_preview': True
        }
        return self.push('post', url, data=data)
