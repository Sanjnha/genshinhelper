from . import notifiers
from ._version import __version__
from .config import config
from .genshin import YuanshenCheckin, GenshinCheckin
from .utils import log, get_cookies
from .weibo import SuperTopicCheckin, RedemptionCode

message_box = []
exitcode = 0


def __run_sign(name, cookies, func):
    success_count = 0
    failure_count = 0
    if not cookies:
        return success_count, failure_count

    global message_box, exitcode

    account_count = len(cookies)
    account = 'account' if account_count == 1 else 'accounts'

    log.info(f'You have {account_count} 「{name}」 {account} configured.')
    message = []
    for i, cookie in enumerate(cookies, start=1):
        log.info(f'Preparing to perform tasks for account {i}...')
        try:
            result = func(cookie).run()
            result = f'👻 No.{i}:\n    {result}\n'
            message.append(result)
            success_count += 1
        except Exception as e:
            result = f'👻 No.{i}:\n    {e}\n'
            log.exception(result)
            # log.error(result)
            message.append(result)
            failure_count += 1
            exitcode = -1
        continue

    message_box.append(f'〓{name}〓')
    message_box.append(f'🔰 ✔ {success_count} · ✖ {failure_count}')
    message_box.append((''.join(message)))

    return success_count, failure_count


def main():
    log.info(f'🌀 genshinhelper v{__version__}')
    log.info('Running process...')

    global message_box

    # Use markdown code block
    message_box.append('```')

    # miHoYo bbs
    mys_cookies = get_cookies(config.COOKIE_MIHOYOBBS)
    mys_success_count, mys_failure_count = __run_sign('米游社原神签到', mys_cookies, YuanshenCheckin)

    # HoYoLAB Community
    lab_cookies = get_cookies(config.COOKIE_HOYOLAB)
    lab_success_count, lab_failure_count = __run_sign('HoYoLAB Community', lab_cookies, GenshinCheckin)

    # Weibo Super Topic
    wb_cookies = get_cookies(config.COOKIE_WEIBO)
    wb_success_count, wb_failure_count = __run_sign('微博超话签到', wb_cookies, SuperTopicCheckin)

    # ka.sina.com.cn
    ka_cookies = get_cookies(config.COOKIE_KA)
    ka_success_count, ka_failure_count = __run_sign('微博原神兑换码', ka_cookies, RedemptionCode)

    message_box.append('```')
    message_box = '\n'.join(message_box)

    success_count = mys_success_count + lab_success_count + wb_success_count + ka_success_count
    failure_count = mys_failure_count + lab_failure_count + wb_failure_count + ka_failure_count

    # Remove '```' and print result to console
    log.info('RESULT:' + message_box.split('```')[1])

    try:
        notifiers.send2all(
            status=f' ✔ {success_count} · ✖ {failure_count}', desp=message_box)
    except Exception as e:
        log.error(e)

    if exitcode != 0:
        log.error(f'Process finished with exit code {exitcode}')
        exit(exitcode)
    log.info('End of process run')
