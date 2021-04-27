简体中文 | [English](./README.en-US.md)

<div align="center"> 
<h1>genshinhelper</h1>
<p>Automatically get Genshin Impact daily check-in rewards.</p>
<p><a href="https://qm.qq.com/cgi-bin/qm/qr?k=_M9lYFxkYD7yQQR2btyG3pkZWFys_I-l&authKey=evGDzE2eFVBm46jsHpgcWrokveg70Z9GKl3H45o0oJuia620UGeO27lDPG9gKb/2&noverify=0">QQ Group</a> | <a href="https://discord.gg/p28845gGfv">Discord</a> | <a href="https://t.me/genshinhelper">Telegram</a></p>

![Genshin Impact Helper](https://i.loli.net/2020/11/18/3zogEraBFtOm5nI.jpg)

</div>

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## 📖 目录

- [🌀1. 前言](#1-%E5%89%8D%E8%A8%80)
- [💡2. 特性](#2-%E7%89%B9%E6%80%A7)
- [🛠3. 配置](#%F0%9F%9B%A03-%E9%85%8D%E7%BD%AE)
  - [3.1 获取参数](#31-%E8%8E%B7%E5%8F%96%E5%8F%82%E6%95%B0)
  - [3.2 使用参数](#32-%E4%BD%BF%E7%94%A8%E5%8F%82%E6%95%B0)
  - [3.3 配置多账号](#33-%E9%85%8D%E7%BD%AE%E5%A4%9A%E8%B4%A6%E5%8F%B7)
- [📐4. 部署](#4-%E9%83%A8%E7%BD%B2)
  - [4.1 Docker](#41-docker)
  - [4.2 Python Package](#42-python-package)
  - [4.3 Tencent Cloud SCF (Serverless)](#43-tencent-cloud-scf-serverless)
  - [4.4 Alibaba Cloud FC (Serverless)](#44-alibaba-cloud-fc-serverless)
  - [4.5 GitHub Actions (Serverless)](#45-github-actions-serverless)
- [🔔5. 订阅](#5-%E8%AE%A2%E9%98%85)
- [🧬6. 环境变量](#%F0%9F%A7%AC6-%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F)
- [🎉7. 致谢](#7-%E8%87%B4%E8%B0%A2)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## 🌀1. 前言

> genshinhelper 可以自动化为你获取原神每日福利

原神是少有的游戏本体和签到福利分离的游戏，玩家为了签到还要额外下载米游社 App。

平心而论，目前的每日签到奖励真的不咋地，都知道是蚊子腿。事实上，你完全可以选择无视签到，不签也没啥大的损失；或者选择手动签到，但这样的话哪天忘记打卡了就很头疼。

为了原石、摩拉和紫色经验书等签到奖励，这个项目应运而生，可以实现自动每日签到。

	如果觉得本项目对你有帮助，请顺手点个 ⭐Star 吧QAQ ♥

## 💡2. 特性

- [x] **米游社原神每日签到**
- [x] **米游社国际版(HoYoLAB)原神每日签到**
- [x] **微博超话签到** 支持任意 IP 签到
- [x] **原神超话功能** 活动监测 + 领兑换码 + 多方推送
- [x] **支持订阅推送** 可选多种订阅方式，每天将签到结果推送给用户
- [x] **支持多个账号** 不同账号的 Cookie 值之间用`#`分隔，如：`<cookie1>#<cookie2>#<cookie3>`
- [x] **支持多个角色** 支持绑定官服和B站服的米游社账号
- [ ] **虎扑原神签到**

## 🛠3. 配置

部署之前请先获取相关自定义配置，包括目标网站的 Cookies 和各种订阅方式的 Token 或 Key 等参数。

### 3.1 获取参数

各种订阅方式的 Token 或 Key 可以在对应网站的使用文档中找到获取方法，这里不再赘述；而目标网站的 Cookies 需要自己获取。

下面演示如何获取米游社的 Cookie，其他网站同理：

1. 浏览器**无痕模式**打开 [https://bbs.mihoyo.com/ys/](https://bbs.mihoyo.com/ys/) ，登录账号
2. 按`F12`，打开`开发者工具`，找到并点击`Network`
3. 按`F5`刷新页面，按下图复制 Cookie：

![How to get mys cookie](https://i.loli.net/2020/10/28/TMKC6lsnk4w5A8i.png)

当触发`Debugger`时，可尝试按`Ctrl + F8`关闭，然后再次刷新页面，最后复制 Cookie。也可以使用另一种方法：

1. 复制代码 `var cookie=document.cookie;var ask=confirm('Cookie:'+cookie+'\n\nDo you want to copy the cookie to the clipboard?');if(ask==true){copy(cookie);msg=cookie}else{msg='Cancel'}`
2. 浏览器**无痕模式**打开 [https://bbs.mihoyo.com/ys/](https://bbs.mihoyo.com/ys/) ，登录账号
3. 按`F12`，打开`开发者工具`，找到并点击`Console`
4. 控制台粘贴代码并运行，获得类似`Cookie:xxxxxx`的输出信息
5. `xxxxxx`部分即为所需复制的 Cookie，点击确定复制

> 提示：获取的米游社/米游社国际版 Cookie 应包含`account_id`和`cookie_token`两个字段，否则视为获取失败。这时可尝试退出账号，打开无痕模式重新获取。

特别地，微博还要额外的`aid`和`s`参数，需要在 微博国际版App 抓包取得。

### 3.2 使用参数

项目有两种使用自定义配置的方式：

- 环境变量

直接将你的配置写入环境变量，变量列表可参考[环境变量](#6-环境变量)。

- 配置文件

推荐将配置文件模板 [config.example.json](genshinhelper/config/config.example.json) 拷贝并重命名为`config.json`再填入你的配置；也可以直接使用 [config.example.json](genshinhelper/config/config.example.json) 文件。用法可参考[配置文件文档](genshinhelper/config/README.md)。

### 3.3 配置多账号

Cookie 支持配置多个，不同账号的 Cookie 值之间用`#`分隔，如：`COOKIE_MIHOYOBBS="<cookie1>#<cookie2>#<cookie3>"`

## 📐4. 部署

### 4.1 Docker 

Docker Hub: [https://registry.hub.docker.com/r/yindan/genshinhelper](https://registry.hub.docker.com/r/yindan/genshinhelper)

```
# 安装 Docker
wget -qO- get.docker.com | bash

# 启动 Docker
systemctl start docker

# 设置 Docker 开机自启
systemctl enable docker

# 基本使用
# 需要什么功能就用 -e 变量名="变量值" 的形式添加，此处以米游社(COOKIE_MIHOYOBBS)和Server酱(SCKEY)做演示
docker run -d --name=genshinhelper \
-e COOKIE_MIHOYOBBS="<COOKIE_MIHOYOBBS>" \
-e SCKEY="<SCKEY>" \
--restart always \
yindan/genshinhelper:latest

# 高级使用
# 使用 -e CRON_SIGNIN="0 7 * * *" 的形式自定义运行时间，所用时间为北京时间
docker run -d --name=genshinhelper \
-e COOKIE_MIHOYOBBS="<COOKIE_MIHOYOBBS>" \
-e SCKEY="<SCKEY>" \
-e CRON_SIGNIN="0 7 * * *" \
--restart always \
yindan/genshinhelper:latest

# 使用 config.json
# 假设你的配置文件是 `/etc/genshin/config.json`
docker run -d --name=genshinhelper \
-e COOKIE_MIHOYOBBS="<COOKIE_MIHOYOBBS>" \
-e SCKEY="<SCKEY>" \
-e CRON_SIGNIN="0 7 * * *" \
-v /etc/genshin:/app/genshinhelper/config \
--restart always \
yindan/genshinhelper:latest

# 查看日志
docker logs -f genshinhelper
```

### 4.2 Python Package

```
pip install genshinhelper

# 添加相关环境变量后执行
python genshinhelper
```

### 4.3 Tencent Cloud SCF (Serverless)

> 提示：Cron表达式为 7 位数

- 前往 [releases](https://github.com/agbulletz/genshinhelper/releases) 页面，下载最新的`genshinhelper-xxx-serverless.zip`压缩包
- 前往 [云函数 SCF 管理控制台](https://console.cloud.tencent.com/scf/) -->`函数服务`-->`新建`-->`自定义创建`-->`基础配置`-->`本地上传zip包`-->`上传`-->`本地上传zip包`--> 选择下载的`genshinhelper-xxx-serverless.zip`压缩包-->`完成`

![2021-4-27 16-37-59.png](https://i.loli.net/2021/04/27/2gHPKxcsqbwhMTN.png)

- 前往`genshinhelper`-->`函数管理`-->`函数配置`-->`编辑`

![2021-4-27 17-14-54.png](https://i.loli.net/2021/04/27/5uo7nx3zMBhUbXg.png)

- 修改`执行超时时间`为`300`秒，在`环境变量`添加环境变量，变量列表可参考[环境变量](#6-环境变量)。

![2021-4-27 17-16-28.png](https://i.loli.net/2021/04/27/nTrm8GdFVXl9xsI.png)

- 前往`genshinhelper`-->`触发管理`-->`新建触发器`--> 按下图进行配置：

![2021-4-27 16-45-40.png](https://i.loli.net/2021/04/27/9yxvGT73itAHRqC.png)

### 4.4 Alibaba Cloud FC (Serverless)

> 提示：Cron表达式为 6 位数

International: https://www.alibabacloud.com/zh/product/function-compute

中国站: https://cn.aliyun.com/product/fc

- 前往 [releases](https://github.com/agbulletz/genshinhelper/releases) 页面，下载最新的`genshinhelper-xxx-serverless.zip`压缩包
- 前往 [函数计算 FC 管理控制台](https://fc.console.aliyun.com/fc/) -->`新建函数`-->`事件函数`-->`代码包上传`-->`上传代码`--> 选择下载的`genshinhelper-xxx-serverless.zip`压缩包 --> 按下图进行配置，注意函数入口为`index.main_handler` -->`新建`

![aly1.png](https://i.loli.net/2021/04/27/NyW1EGML4cHgo6Z.png)

- 前往`genshinhelper` -->`概览`-->`修改配置`

![aly2.png](https://i.loli.net/2021/04/27/1x2kbsVjMUXlwRv.png)

- 下拉找到`环境变量`添加环境变量，变量列表可参考[环境变量](#6-环境变量)。

![aly3.png](https://i.loli.net/2021/04/27/e7GTEumrIh5q3Kt.png)

- 前往`genshinhelper`-->`触发器`-->`创建触发器`--> 按下图进行配置：

![aly4.png](https://i.loli.net/2021/04/27/5Oj2acDs3VCture.png)

### 4.5 GitHub Actions (Serverless)

> 提示：Cron表达式为 5 位数

项目地址：https://github.com/agbulletz/genshinhelper

- 点击右上角`Fork`将 [agbulletz/genshinhelper](https://github.com/agbulletz/genshinhelper) fork 到自己的账号下

![fork](https://i.loli.net/2020/10/28/qpXowZmIWeEUyrJ.png)

- 转到 fork 仓库，创建genshinhelper/.github/workflows/main.yml`文件

```yaml
name: "Genshin Impact Helper"

on:
  schedule:
    - cron: "0 22 * * *"  # scheduled at 06:00 (UTC+8) everyday
  workflow_dispatch:

env:
  TZ: 'Asia/Shanghai'

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout master
        uses: actions/checkout@v2
        with:
          fetch-depth: 0
          # ref: master

      - name: Set up python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8

      - name: Random sleep
        if: github.event_name == 'schedule'
        run: sleep $(shuf -i 10-30 -n 1)

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run sign
        env:
          COOKIE_MIHOYOBBS: ${{ secrets.COOKIE_MIHOYOBBS }}
          COOKIE_HOYOLAB: ${{ secrets.COOKIE_HOYOLAB }}
          COOKIE_WEIBO: ${{ secrets.COOKIE_WEIBO }}
          WEIBO_INTL_AID: ${{ secrets.WEIBO_INTL_AID }}
          WEIBO_INTL_S: ${{ secrets.WEIBO_INTL_S }}
          COOKIE_KA: ${{ secrets.COOKIE_KA }}
          BARK_KEY: ${{ secrets.BARK_KEY }}
          BARK_SOUND: ${{ secrets.BARK_SOUND }}
          COOL_PUSH_SKEY: ${{ secrets.COOL_PUSH_SKEY }}
          COOL_PUSH_MODE: ${{ secrets.COOL_PUSH_MODE }}
          CUSTOM_NOTIFIER: ${{ secrets.CUSTOM_NOTIFIER }}
          DD_BOT_TOKEN: ${{ secrets.DD_BOT_TOKEN }}
          DD_BOT_SECRET: ${{ secrets.DD_BOT_SECRET }}
          DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
          IGOT_KEY: ${{ secrets.IGOT_KEY }}
          PUSH_PLUS_TOKEN: ${{ secrets.PUSH_PLUS_TOKEN }}
          PUSH_PLUS_USER: ${{ secrets.PUSH_PLUS_USER }}
          SCKEY: ${{ secrets.SCKEY }}
          SCTKEY: ${{ secrets.SCTKEY }}
          TG_BOT_API: ${{ secrets.TG_BOT_API }}
          TG_BOT_TOKEN: ${{ secrets.TG_BOT_TOKEN }}
          TG_USER_ID: ${{ secrets.TG_USER_ID }}
          WW_ID: ${{ secrets.WW_ID }}
          WW_APP_SECRET: ${{ secrets.WW_APP_SECRET }}
          WW_APP_USERID: ${{ secrets.WW_APP_USERID }}
          WW_APP_AGENTID: ${{ secrets.WW_APP_AGENTID }}
          WW_BOT_KEY: ${{ secrets.WW_BOT_KEY }}
          
        run: |
          python3 genshinhelper
```

- 回到项目页面，依次点击`Settings`-->`Secrets`-->`New secret`

![new-secret.png](https://i.loli.net/2020/10/28/sxTuBFtRvzSgUaA.png)

- 依次建立 secret，此步骤为添加环境变量，变量列表可参考[环境变量](#6-环境变量)，最后点击Add secret

![add-secret](https://i.loli.net/2020/10/28/sETkVdmrNcCUpgq.png)

- 返回项目主页面，点击上方的`Actions`，再点击左侧的`Genshin Impact Helper`，再点击`Run workflow`

![run](https://i.loli.net/2020/10/28/5ylvgdYf9BDMqAH.png)

Actions 默认为关闭状态，Fork 之后需要手动执行一次，若成功运行其才会激活。

## 🔔5. 订阅

支持 [Bark App](https://apps.apple.com/us/app/bark-%E7%BB%99%E4%BD%A0%E7%9A%84%E6%89%8B%E6%9C%BA%E5%8F%91%E6%8E%A8%E9%80%81/id1403753865) 、
酷推、钉钉机器人、Discord、iGot聚合推送、pushplus、Server酱、Telegram robot、企业微信应用、企业微信机器人和自定义推送
单个或多个推送，通过配置环境变量或填写配置文件开启对应推送方式，变量名称列表详见下文`环境变量`部分内容。

- 自定义推送

```json
{
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
}
```
```
Custom notifier:
    method:                 Required, the request method. Default: post.
    url:                    Required, the full custom push link.
    data:                   Optional, the data to sent. default: {}, you can add additional parameters.
    retcode_key:            Required, the key of the status code returned by the response body.
    retcode_value:          Required, the value of the status code returned by the response body.
    data_type:              Optional, the way to send data, choose from params|json|data, default: data.
    merge_title_and_desp:   Optional, if or not the title (application name + running status) and the running result will be merged. Default: false.
    set_data_title:         Required, the key of the message title in the data of the push method.
    set_data_sub_title:     Optional, the key of the message body in the push data.
    set_data_desp:          Optional, the key of the message body in the push data.

自定义推送:
    method:                 必填,请求方式.默认: post.
    url:                    必填,完整的自定义推送链接.
    data:                   选填,发送的data.默认为空,可自行添加额外参数.
    retcode_key:            必填,响应体返回的状态码的key.
    retcode_value:          必填,响应体返回的状态码的value.
    data_type:              选填,发送data的方式,可选params|json|data,默认: data.
    merge_title_and_desp:   选填,是否将标题(应用名+运行状态)和运行结果合并.默认: false.
    set_data_title:         必填,推送方式data中消息标题的key.
    set_data_sub_title:     选填,推送方式data中消息正文的key.有的推送方式正文的key有次级结构,需配合set_data_title构造子级,与set_data_desp互斥.
                                例如: 企业微信中,set_data_title填text,set_data_sub_title填content.
    set_data_desp:          选填,推送方式data中消息正文的key.例如: server酱的为desp.
                                与set_data_sub_title互斥,两者都填则本项不生效.
```
例子：
写一个 ServerChan 的自定义推送。

查看文档得到 ServerChan 推送所需要的信息：
需要的`url`形式为：`https://sc.ftqq.com/{SCKEY}.send`
发送的`data`形式为：`{'text': test','desp':desp}`
消息发送成功响应体为：`{'errno': 0, 'errmsg': 'OK'}`

自定义推送配置如下：
```
{
    "method":"post",
    "url":"https://sc.ftqq.com/{直接填写你的SCKEY}.send",
    "data":{
      
    },
    "retcode_key":"errno",
    "retcode_value":0,
    "data_type":"data",
    "merge_title_and_desp":true,
    "set_data_title":"test",
    "set_data_sub_title":"",
    "set_data_desp":"desp"
}
```
> 提示：若开启订阅推送，无论成功与否，都会收到推送通知。

## 🧬6. 环境变量

下表罗列了本项目所用到的全部环境变量

| **Variable Name** | **Required** | **The name in the config.json** | **Default**        | **Website**                                           | **Description**                                                                             |
|-------------------|--------------|---------------------------------|--------------------|-------------------------------------------------------|---------------------------------------------------------------------------------------------|
| LANGUAGE          | ❌            | language                        | en-us              |                                                       | Rewards language for HoYoLAB daily check-in.                                                |
| COOKIE_MIHOYOBBS  | ❌            | cookie_mihoyobbs                |                    | https://bbs.mihoyo.com/ys/                            | Cookie from miHoYo bbs.                                                                     |
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

## 🎉7. 致谢

原项目 [y1ndan/genshin-impact-helper](https://github.com/y1ndan/genshin-impact-helper) 于2021.04.02被GitHub屏蔽，至今未取得官方回复。感谢所有为该项目贡献代码的大佬们以及使用该项目的小可爱。

Huge thanks to:
@PomeloWang
@Celeter
@Arondight
@chenkid999
@xe5700
@Renari
@journey-ad
@aflyhorse
@thesadru
@PeterPanZH
@cainiaowu
@alwaysmiddle
@qianxu2001
