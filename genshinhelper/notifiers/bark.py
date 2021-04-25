from urllib import parse

from .basenotifier import BaseNotifier as Base
from ..config import config


class Bark(Base):
    def __init__(self):
        self.name = 'Bark App'
        self.token = config.BARK_KEY
        self.retcode_key = 'code'
        self.retcode_value = 200

    def send(self, text=Base.app, status=Base.status, desp=Base.desp):
        url = f'{config.BARK_KEY}/{text} {status}/{parse.quote(str(desp))}'
        data = {'sound': config.BARK_SOUND}
        return self.push('get', url, params=data)
