from .basenotifier import BaseNotifier as Base
from ..config import config


class PushPlus(Base):
    def __init__(self):
        self.name = 'pushplus'
        self.token = config.PUSH_PLUS_TOKEN
        self.retcode_key = 'code'
        self.retcode_value = 200

    def send(self, text=Base.app, status=Base.status, desp=Base.desp):
        url = 'https://pushplus.hxtrip.com/send'
        data = {
            'token': config.PUSH_PLUS_TOKEN,
            'title': f'{text} {status}',
            'content': desp,
            'topic': config.PUSH_PLUS_USER
        }
        return self.push('post', url, data=data)
