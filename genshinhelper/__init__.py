from time import sleep
from random import randint

from . import notifiers
from ._version import __version__
from .config import config
from .genshin import YuanshenCheckin, GenshinCheckin
from .miyoubi import MiyoubiCheckin
from .utils import log, get_cookies
from .weibo import SuperTopicCheckin, RedemptionCode
from .utils import _


banner = """
░█▀▀▀░█▀▀░█▀▀▄░█▀▀░█░░░░░▀░░█▀▀▄░█░░░░█▀▀░█░░▄▀▀▄░█▀▀░█▀▀▄
░█░▀▄░█▀▀░█░▒█░▀▀▄░█▀▀█░░█▀░█░▒█░█▀▀█░█▀▀░█░░█▄▄█░█▀▀░█▄▄▀
░▀▀▀▀░▀▀▀░▀░░▀░▀▀▀░▀░░▀░▀▀▀░▀░░▀░▀░░▀░▀▀▀░▀▀░█░░░░▀▀▀░▀░▀▀
"""
exit_code = 0
tasks = {
    'mihoyo': [
        '原神签到福利',
        get_cookies(config.COOKIE_MIHOYOBBS),
        YuanshenCheckin
    ],
    'miyoubi': [
        '米游币签到姬',
        get_cookies(config.COOKIE_MIYOUBI),
        MiyoubiCheckin
    ],
    'hoyolab': [
        'HoYoLAB Community',
        get_cookies(config.COOKIE_HOYOLAB),
        GenshinCheckin
    ],
    'weibo': [
        '微博超话签到',
        get_cookies(config.COOKIE_WEIBO),
        SuperTopicCheckin
    ],
    'ka': [
        '原神超话监测',
        get_cookies(config.COOKIE_KA),
        RedemptionCode
    ]
}


def __run_sign(name, cookies, func):
    success_count = 0
    failure_count = 0
    if not cookies:
        return [success_count, failure_count]

    account_count = len(cookies)
    account_str = 'account' if account_count == 1 else 'accounts'
    log.info(_('You have {account_count} 「{name}」 {account_str} configured.').format(
        account_count=account_count, name=name, account_str=account_str
        ))
    global exit_code
    result_list = []
    for i, cookie in enumerate(cookies, start=1):
        log.info(_('Preparing to perform tasks for account {i}...').format(i=i))
        try:
            result = func(cookie).run()
            success_count += 1
        except Exception as e:
            result = e
            log.exception('TRACEBACK')
            failure_count += 1
            exit_code = -1
        finally:
            result = f'🌈 No.{i}:\n    {result}\n'
            result_list.append(result)
        continue

    message_box = [
        success_count,
        failure_count,
        f'🏆 {name}',
        f'☁️ ✔ {success_count} · ✖ {failure_count}',
        ''.join(result_list)
    ]
    return message_box


def main():
    log.info(banner)
    log.info(f'🌀 genshinhelper v{__version__}')

    if config.RUN_ENV == 'prod':
        sleep_secs = randint(10, config.MAX_SLEEP_SECS)
        log.info(_('Sleep for {} seconds...').format(sleep_secs))
        sleep(sleep_secs)

    log.info(_('Starting...'))

    result = {i[0]: __run_sign(i[1][0], i[1][1], i[1][2]) for i in tasks.items()}
    total_success = sum([i[0] for i in result.values()])
    total_failure = sum([i[1] for i in result.values()])
    message = sum([i[2::] for i in result.values()], [])
    tip = _('WARNING: Please configure environment variables or config.json file first!\n')
    message_box = '\n'.join(message) if message else tip

    log.info(_('RESULT:\n') + message_box)
    # The ``` is added to use markdown code block
    markdown_message = f'```\n{message_box}```'
    if message_box != tip:
        try:
            notifiers.send2all(
                status=f' ✔ {total_success} · ✖ {total_failure}', desp=markdown_message)
        except Exception as e:
            log.exception('TRACEBACK')

    if exit_code != 0:
        log.error(_('Process finished with exit code {exit_code}').format(exit_code=exit_code))
        exit(exit_code)
    log.info(_('End of process run'))

