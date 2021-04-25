## Configuration file template

[/genshinhelper/config/config.example.json](/genshinhelper/config/config.example.json)

It is recommended to copy and rename `config.example.json` to `config.json` before use configuration file.

### config.example.json

```json
{
    "//":"Rewards language for HoYoLAB daily check-in.",
    "language":"en-us",
    "//":"Please split cookies with `#` if you have multiple cookies. For example: 1#2#3#4.",
    "cookies":{
        "//":"Cookie from miHoYo bbs: https://bbs.mihoyo.com/ys/",
        "cookie_mihoyobbs":"",
        "//":"Cookie from HoYoLAB community: https://www.hoyolab.com/genshin/",
        "cookie_hoyolab":"",
        "//":"Cookie from Weibo intl app. Cookie from https://m.weibo.cn might work.",
        "cookie_weibo":"",
        "//":"Weibo intl app's aid-parameters.",
        "weibo_intl_aid":"",
        "//":"Weibo intl app's s-parameters.",
        "weibo_intl_s":"",
        "//":"Cookie from https://ka.sina.com.cn/",
        "cookie_ka":""
    },
    "notifiers":{
        "//":"iOS Bark app's IP or device code. For example: https://api.day.app/xxxxxx",
        "bark_key":"",
        "//":"iOS Bark app's notification sound. Default: healthnotification",
        "bark_sound":"healthnotification",
        "//":"SKEY for Cool Push. See: https://cp.xuthus.cc/",
        "cool_push_skey":"",
        "//":"Push method for Cool Push. Choose from send(私聊)|group(群组)|wx(微信). Default: send",
        "cool_push_mode":"send",
        "//":"Custom notifier configuration",
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
        "//":"钉钉机器人WebHook地址中access_token后的字段.",
        "dingtalk_bot_token":"",
        "//":"钉钉加签密钥.在机器人安全设置页面,加签一栏下面显示的以SEC开头的字符串.",
        "dingtalk_bot_secret":"",
        "//":"Webhook of Discord.",
        "discord_webhook":"",
        "//":"KEY for iGot. For example: https://push.hellyw.com/xxxxxx",
        "igot_key":"",
        "//":"pushplus 一对一推送或一对多推送的token.不配置push_plus_user则默认为一对一推送.详见文档: https://www.pushplus.plus/doc/",
        "push_plus_token":"",
        "//":"pushplus 一对多推送的群组编码.在'一对多推送'->'您的群组'(如无则新建)->'群组编码'里查看,如果是创建群组人,也需点击'查看二维码'扫描绑定,否则不能接收群组消息.",
        "push_plus_user":"",
        "//":"SCKEY for ServerChan. See: https://sc.ftqq.com/3.version",
        "server_chan_key":"",
        "//":"SENDKEY for ServerChanTurbo. See: https://sct.ftqq.com/",
        "server_chan_turbo_key":"",
        "//":"Telegram robot api address. Default: api.telegram.org",
        "telegram_bot_api":"api.telegram.org",
        "//":"Telegram robot token. Generated when requesting a bot from @botfather",
        "telegram_bot_token":"",
        "//":"User ID of the Telegram push target.",
        "telegram_user_id":"",
        "//":"企业微信的企业ID(corpid).在'管理后台'->'我的企业'->'企业信息'里查看.详见文档: https://work.weixin.qq.com/api/doc/90000/90135/90236",
        "wechat_work_id":"",
        "//":"企业微信应用的secret.在'管理后台'->'应用与小程序'->'应用'->'自建',点进某应用里查看.",
        "wechat_work_app_secret":"",
        "//":"企业微信应用推送对象的用户ID.在'管理后台'->' 通讯录',点进某用户的详情页里查看.默认: @all",
        "wechat_work_app_userid":"@all",
        "//":"企业微信应用的agentid.在'管理后台'->'应用与小程序'->'应用',点进某应用里查看.",
        "wechat_work_app_agentid":"",
        "//":"企业微信机器人WebHook地址中key后的字段.详见文档: https://work.weixin.qq.com/api/doc/90000/90136/91770",
        "wechat_work_bot_key":""
    }
}
```
### Custom notifier configuration

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
