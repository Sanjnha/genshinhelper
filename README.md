English | [简体中文](https://www.yindan.me/tutorial/genshin-impact-helper.html)

<div align="center"> 
<h1>genshinhelper</h1>
<p>Automatically get Genshin Impact daily check-in rewards.</p>

[![GitHub stars](https://img.shields.io/github/stars/y1ndan/genshinhelper?style=flat-square)](https://github.com/y1ndan/genshinhelper/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/y1ndan/genshinhelper?style=flat-square)](https://github.com/y1ndan/genshinhelper/network)
[![GitHub issues](https://img.shields.io/github/issues/y1ndan/genshinhelper?style=flat-square)](https://github.com/y1ndan/genshinhelper/issues)
[![Docker stars](https://img.shields.io/docker/stars/yindan/genshinhelper?style=flat-square)](https://registry.hub.docker.com/r/yindan/genshinhelper)
![Docker pulls](https://img.shields.io/docker/pulls/yindan/genshinhelper?style=flat-square)
[![PyPI version](https://img.shields.io/pypi/v/genshinhelper?style=flat-square)](https://pypi.org/project/genshinhelper/#history)
[![PyPI downloads](https://img.shields.io/pypi/dm/genshinhelper?style=flat-square)](https://pypi.org/project/genshinhelper)
[![QQ Group](https://img.shields.io/badge/chat-130516740-0d86d7?style=flat-square)](https://qm.qq.com/cgi-bin/qm/qr?k=_M9lYFxkYD7yQQR2btyG3pkZWFys_I-l)
[![Discord](https://img.shields.io/badge/chat-discord-0d86d7?style=flat-square)](https://discord.gg/p28845gGfv)
[![Telegram](https://img.shields.io/badge/chat-telegram-0d86d7?style=flat-square)](https://t.me/genshinhelper)

```

░█▀▀▀░█▀▀░█▀▀▄░█▀▀░█░░░░░▀░░█▀▀▄░█░░░░█▀▀░█░░▄▀▀▄░█▀▀░█▀▀▄
░█░▀▄░█▀▀░█░▒█░▀▀▄░█▀▀█░░█▀░█░▒█░█▀▀█░█▀▀░█░░█▄▄█░█▀▀░█▄▄▀
░▀▀▀▀░▀▀▀░▀░░▀░▀▀▀░▀░░▀░▀▀▀░▀░░▀░▀░░▀░▀▀▀░▀▀░█░░░░▀▀▀░▀░▀▀

```

</div>

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
	* [Docker](#docker)
	* [PyPI Package](#pypi-package)
	* [Serverless](#serverless)
		+ [Tencent Cloud SCF](#tencent-cloud-scf)
		+ [Alibaba Cloud FC](#alibaba-cloud-fc)
- [Configuration](#configuration)
	* [Environment Variables](#environment-variables)
	* [Configuration file](#configuration-file)
	* [Multiple accounts](#multiple-accounts)
- [Contributing](#contributing)
- [Help and Support](#help-and-support)
- [Acknowledgements](#acknowledgements)
- [License](#license)

`If this project is helpful to you, please give us a ⭐️Star QAQ ♥`

## Features

- [x] **miHoYo BBS Genshin Impact daily check-in**
- [x] **HoYoLAB Community Genshin Impact daily check-in**
- [x] **Weibo super topic daily check-in**
- [x] **Support subscription push**
- [x] **Support multiple accounts**
- [x] **Support multiple roles (CN Server)**

## Installation

This project uses [Docker](https://www.docker.com/) or [Python3](https://www.python.org/). Go check it out if you don't have one of them locally installed.

- Docker

You can use the following command to pull the image:

```sh
$ docker pull yindan/genshinhelper
```

This pulls the latest release of `genshinhelper`.

It can be found at [Docker Hub](https://registry.hub.docker.com/r/yindan/genshinhelper/).

- PyPI Package

You can also use the [pypi package](https://pypi.org/project/genshinhelper/):

```sh
$ pip install genshinhelper
```

## Usage

### Docker

In the following commands, `COOKIE_MIHOYOBBS` is the variable name and `<COOKIE_MIHOYOBBS>` is your `COOKIE_MIHOYOBBS` value. The same goes for `DISCORD_WEBHOOK` and so on.

You can find all the environment variables used in this project in the [Configuration](#configuration) section.

- Basic usage

```sh
$ docker run -d --name=genshinhelper \
-e COOKIE_MIHOYOBBS="<COOKIE_MIHOYOBBS>" \
-e DISCORD_WEBHOOK="<DISCORD_WEBHOOK>" \
--restart always \
yindan/genshinhelper:latest
```

- Advanced usage

Docker triggers tasks at `6:00` (UTC+8) every day by default. Use the `CRON_SIGNIN` variable to customize the trigger time.

> Tips: Trigger time according to UTC+8

```sh
$ docker run -d --name=genshinhelper \
-e COOKIE_MIHOYOBBS="<COOKIE_MIHOYOBBS>" \
-e DISCORD_WEBHOOK="<DISCORD_WEBHOOK>" \
-e CRON_SIGNIN="0 7 * * *" \
--restart always \
yindan/genshinhelper:latest
```

If you want to use the `config.json` configuration file, use the following command to map the relevant folder.

Assuming your configuration file is located at `/etc/genshin/config.json`.

```sh
$ docker run -d --name=genshinhelper \
-e COOKIE_MIHOYOBBS="<COOKIE_MIHOYOBBS>" \
-e DISCORD_WEBHOOK="<DISCORD_WEBHOOK>" \
-e CRON_SIGNIN="0 7 * * *" \
-v /etc/genshin:/app/genshinhelper/config \
--restart always \
yindan/genshinhelper:latest
```

- Useful commands

```
# Logs
$ docker logs -f genshinhelper --tail 100

# Restart
$ docker restart genshinhelper

# Update
$ docker pull yindan/genshinhelper
$ docker rm -f genshinhelper
# Re-create the container with the latest image according to basic usage or Advanced usage.

# Uninstall
$ docker rm -f genshinhelper
$ docker image rm genshinhelper
```

### PyPI Package

You **must add environment variables** in host at first. See [Configuration](#configuration) for more details.

The following command assume that you have already added the environment variables.

```sh
$ python -m genshinhelper
```

### Serverless

If you don't have a host, you can try using serverless deployment. It can help you to automatically check-in every day.

You need to download the latest `genshinhelper-xxx-serverless.zip` serverless zip file at first. The entry point of the zip file is `index.main_handler`.

#### Tencent Cloud SCF

> Tips: Cron expressions are 7 digits

[International](https://intl.cloud.tencent.com/product/scf) | [中国站](https://cloud.tencent.com/product/scf)

- Go to [云函数 SCF 管理控制台](https://console.cloud.tencent.com/scf/) → `函数服务` → `新建` → `自定义创建` → `基础配置` → `本地上传zip包` → `上传` → `本地上传zip包` → Select the downloaded file `genshinhelper-xxx-serverless.zip` → `完成`

![SCF_upload](https://i.loli.net/2021/04/27/2gHPKxcsqbwhMTN.png)

- Go to `genshinhelper` → `函数管理` → `函数配置` → `编辑`

![SCF_edit](https://i.loli.net/2021/04/27/5uo7nx3zMBhUbXg.png)

- Modify `执行超时时间` to `300` seconds and add environment variables in `环境变量`. The list of environment variables can be found in the [Configuration](#configuration) section.

![SCF_add_environment_variables](https://i.loli.net/2021/04/27/nTrm8GdFVXl9xsI.png)

- Go to `genshinhelper` → `触发管理` → `新建触发器` → Configure as shown below:

![SCF_Triggers](https://i.loli.net/2021/04/27/9yxvGT73itAHRqC.png)

#### Alibaba Cloud FC

> Tips: Cron expressions are 6 digits

[International](https://www.alibabacloud.com/zh/product/function-compute) | [中国站](https://cn.aliyun.com/product/fc)

 - Go to [函数计算 FC 管理控制台](https://fc.console.aliyun.com/fc/) → `新建函数` → `事件函数` → `代码包上传` → `上传代码` → Select the downloaded file `genshinhelper-xxx-serverless.zip` → Configure as shown below. Note that the entry point is `index.main_handler` → `新建`

![FC_upload](https://i.loli.net/2021/04/27/NyW1EGML4cHgo6Z.png)

- Go to `genshinhelper` → `概览` → `修改配置`

![FC_edit](https://i.loli.net/2021/04/27/1x2kbsVjMUXlwRv.png)

- Scroll down and find `环境变量` to add environment variables. The list of environment variables can be found in the [Configuration](#configuration) section.

![FC_add_environment_variables](https://i.loli.net/2021/04/27/e7GTEumrIh5q3Kt.png)

- Go to `genshinhelper` → `触发器` → `创建触发器` → Configure as shown below:

![FC_Triggers](https://i.loli.net/2021/04/27/5Oj2acDs3VCture.png)

## Configuration

The project has two ways of using custom configurations.

### Environment Variables

You can write your configuration directly into the environment variables.

The following table lists all the environment variables used in this project:

<details>
<summary>Click here</summary>

| **Variable Name** | **Required** | **The name in the config.json** | **Default**        | **Website**                                           | **Description**                                                                             |
|-------------------|--------------|---------------------------------|--------------------|-------------------------------------------------------|---------------------------------------------------------------------------------------------|
| LANGUAGE          | ❌            | language                        | en-us              |                                                       | Rewards language for HoYoLAB daily check-in.                                                |
| COOKIE_MIHOYOBBS  | ❌            | cookie_mihoyobbs                |                    | https://bbs.mihoyo.com/ys/                            | Cookie from miHoYo bbs.                                                                     |
| COOKIE_MIYOUBI  | ❌            | cookie_miyoubi                  |                    | https://bbs.mihoyo.com/ys/                            | Cookie from miHoYo bbs.                                                                     |
| COOKIE_HOYOLAB    | ❌            | cookie_hoyolab                  |                    | https://www.hoyolab.com/genshin/                      | Cookie from HoYoLAB community.                                                              |
| COOKIE_WEIBO      | ❌            | cookie_weibo                    |                    | https://m.weibo.cn/                                   | Cookie from Weibo intl app. Cookie from https://m.weibo.cn might work.                      |
| WEIBO_INTL_AID    | ❌            | weibo_intl_aid                  |                    |                                                       | Weibo intl app's aid-parameters.                                                            |
| WEIBO_INTL_S      | ❌            | weibo_intl_s                    |                    |                                                       | Weibo intl app's s-parameters.                                                              |
| COOKIE_KA         | ❌            | cookie_ka                       |                    | https://ka.sina.com.cn/                               | Cookie from https://ka.sina.com.cn/                                                         |
| BARK_KEY          | ❌            | bark_key                        |                    |                                                       | iOS Bark app's IP or device code. For example: https://api.day.app/xxxxxx                   |
| BARK_SOUND        | ❌            | bark_sound                      | healthnotification |                                                       | iOS Bark app's notification sound. Default: healthnotification                              |
| COOL_PUSH_SKEY    | ❌            | cool_push_skey                  |                    | https://cp.xuthus.cc/                                 | SKEY for Cool Push.                                                                         |
| COOL_PUSH_MODE    | ❌            | cool_push_mode                  | send               |                                                       | Push method for Cool Push. Choose from send(私聊),group(群组),wx(微信). Default: send          |
| CRON_SIGNIN       | ❌            |                                 | 0 6 * * *          |                                                       | Docker custom runtime                                                                       |
| CUSTOM_NOTIFIER   | ❌            | custom_notifier                 |                    |                                                       | Custom notifier configuration                                                               |
| DD_BOT_TOKEN      | ❌            | dingtalk_bot_token              |                    |                                                       | 钉钉机器人WebHook地址中access_token后的字段.                                                     |
| DD_BOT_SECRET     | ❌            | dingtalk_bot_secret             |                    |                                                       | 钉钉加签密钥.在机器人安全设置页面,加签一栏下面显示的以SEC开头的字符串.                                   |
| DISCORD_WEBHOOK   | ❌            | discord_webhook                 |                    |                                                       | Webhook of Discord.                                                                         |
| IGOT_KEY          | ❌            | igot_key                        |                    |                                                       | KEY for iGot. For example: https://push.hellyw.com/xxxxxx                                   |
| PUSH_PLUS_TOKEN   | ❌            | push_plus_token                 | 一对一推送           | https://www.pushplus.plus/doc/                        | pushplus 一对一推送或一对多推送的token.不配置push_plus_user则默认为一对一推送.                        |
| PUSH_PLUS_USER    | ❌            | push_plus_user                  |                    |                                                       | pushplus 一对多推送的群组编码.在'一对多推送'->'您的群组'(如无则新建)->'群组编码'里查看,如果是创建群组人,也需点击'查看二维码'扫描绑定,否则不能接收群组消息. |
| SCKEY             | ❌            | server_chan_key                 |                    | https://sc.ftqq.com/3.version/                        | SCKEY for ServerChan.                                                                       |
| SCTKEY            | ❌            | server_chan_turbo_key           |                    | https://sct.ftqq.com/                                 | SENDKEY for ServerChanTurbo.                                                                |
| TG_BOT_API        | ❌            | telegram_bot_api                | api.telegram.org   |                                                       | Telegram robot api address. Default: api.telegram.org                                       |
| TG_BOT_TOKEN      | ❌            | telegram_bot_token              |                    |                                                       | Telegram robot token. Generated when requesting a bot from @botfather                       |
| TG_USER_ID        | ❌            | telegram_user_id                |                    |                                                       | User ID of the Telegram push target.                                                        |
| WW_ID             | ❌            | wechat_work_id                  |                    | https://work.weixin.qq.com/api/doc/90000/90135/90236  | 企业微信的企业ID(corpid).在'管理后台'->'我的企业'->'企业信息'里查看.                                  |
| WW_APP_SECRET     | ❌            | wechat_work_app_secret          |                    |                                                       | 企业微信应用的secret.在'管理后台'->'应用与小程序'->'应用'->'自建',点进某应用里查看.                      |
| WW_APP_USERID     | ❌            | wechat_work_app_userid          | @all               |                                                       | 企业微信应用推送对象的用户ID.在'管理后台'->' 通讯录',点进某用户的详情页里查看.默认: @all                   |
| WW_APP_AGENTID    | ❌            | wechat_work_app_agentid         |                    |                                                       | 企业微信应用的agentid.在'管理后台'->'应用与小程序'->'应用',点进某应用里查看.                            |
| WW_BOT_KEY        | ❌            | wechat_work_bot_key             |                    | https://work.weixin.qq.com/api/doc/90000/90136/91770  | 企业微信机器人WebHook地址中key后的字段.                                                           |

</details>

### Configuration file

It is recommended to copy and rename `config.example.json` to `config.json` before use the configuration file.

A `config.example.json` in JSON like below:

<details>
<summary>Click here</summary>

```json
{
    "language":"en-us",
    "cookies":{
        "cookie_mihoyobbs":"",
        "cookie_miyoubi":"",
        "cookie_hoyolab":"",
        "cookie_weibo":"",
        "weibo_intl_aid":"",
        "weibo_intl_s":"",
        "cookie_ka":""
    },
    "notifiers":{
        "bark_key":"",
        "bark_sound":"healthnotification",
        "cool_push_skey":"",
        "cool_push_mode":"send",
        "custom_notifier":{
            "method":"post",
            "url":"",
            "data":{

            },
            "retcode_key":"",
            "retcode_value":200,
            "data_type":"data",
            "merge_title_and_desp":false,
            "set_data_title":"",
            "set_data_sub_title":"",
            "set_data_desp":""
        },
        "dingtalk_bot_token":"",
        "dingtalk_bot_secret":"",
        "discord_webhook":"",
        "igot_key":"",
        "push_plus_token":"",
        "push_plus_user":"",
        "server_chan_key":"",
        "server_chan_turbo_key":"",
        "telegram_bot_api":"api.telegram.org",
        "telegram_bot_token":"",
        "telegram_user_id":"",
        "wechat_work_id":"",
        "wechat_work_app_secret":"",
        "wechat_work_app_userid":"@all",
        "wechat_work_app_agentid":"",
        "wechat_work_bot_key":""
    }
}
```

</details>

### Multiple accounts

Multiple account cookies need to be separated by "#" symbol. e.g. `COOKIE_MIHOYOBBS="<cookie1>#<cookie2>#<cookie3>"`

## Contributing

Feel free to dive in! Open an [issue](https://github.com/y1ndan/genshinhelper/issues) or submit PRs.

## Help and Support

Please join our chat groups for help and support.

[QQ Group](https://qm.qq.com/cgi-bin/qm/qr?k=_M9lYFxkYD7yQQR2btyG3pkZWFys_I-l) | 
[Discord](https://discord.gg/p28845gGfv) | 
[Telegram](https://t.me/genshinhelper)

## Acknowledgements

The idea for the miyoubi feature is inspired by XiaoMiku01's project [miyoubiAuto](https://github.com/XiaoMiku01/miyoubiAuto).

Huge thanks to the contributors of the [y1ndan/genshin-impact-helper](https://github.com/y1ndan/genshin-impact-helper) project:

- PomeloWang
- Celeter
- Arondight
- chenkid999
- xe5700
- Renari
- journey-ad
- aflyhorse
- thesadru
- PeterPanZH
- cainiaowu
- alwaysmiddle
- qianxu2001

## License

![License](https://img.shields.io/pypi/l/genshinhelper?style=flat-square)


