from .basenotifier import BaseNotifier as Base
from ..config import config


class CoolPush(Base):
    def __init__(self):
        self.name = 'Cool Push'
        self.token = config.COOL_PUSH_SKEY
        self.retcode_key = 'code'
        self.retcode_value = 200

    def send(self, text=Base.app, status=Base.status, desp=Base.desp):
        url = f'https://push.xuthus.cc/{config.COOL_PUSH_MODE}/{config.COOL_PUSH_SKEY}'
        data = f'{text} {status}\n\n{desp}'.encode('utf-8')
        return self.push('post', url, data=data)
