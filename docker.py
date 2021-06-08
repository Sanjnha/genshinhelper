import datetime
import os
import signal
import time
import locale
import gettext

from crontab import CronTab

from genshinhelper import log

time_format = "%Y-%m-%d %H:%M:%S"

_localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locales')
_translate = gettext.translation('genshinhelper', _localedir, fallback=True)
_ = _translate.gettext

def stop_me(_signo, _stack):
    log.info(_("Docker container has stoped...."))
    exit(-1)


def main():
    signal.signal(signal.SIGINT, stop_me)

    log.info(_("Running genshinhelper with docker"))
    env = os.environ
    cron_signin = env["CRON_SIGNIN"]
    cron = CronTab(cron_signin, loop=True, random_seconds=True)

    def next_run_time():
        nt = datetime.datetime.now().strftime(time_format)
        delayt = cron.next(default_utc=False)
        nextrun = datetime.datetime.now() + datetime.timedelta(seconds=delayt)
        nextruntime = nextrun.strftime(time_format)
        log.info(_("Current running datetime: {nt}").format(nt=nt))
        log.info(_("Next run datetime: {nextruntime}").format(nextruntime=nextruntime))

    def sign():
        log.info(_("Starting signing"))
        os.system("python3 genshinhelper")

    sign()
    next_run_time()
    while True:
        ct = cron.next(default_utc=False)
        time.sleep(ct)
        sign()
        next_run_time()


if __name__ == '__main__':
    main()
